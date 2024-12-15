import csv

class Client:
    def __init__(self, file_path):
        self.file_path = file_path

        self.param_list = []
        self.data_user_list = []
        self.user = {}

        self.__get_params()

    def __check_error(self):
        if len(self.param_list) != len(self.data_user_list):
            self.__send_error('в строке не хватает данных')
            return True
        False

    def __send_error(self, text):
        print(F"Ошибка - {text}")

    def __get_params(self):
        file = open(self.file_path, 'r')
        reader = csv.reader(file)
        self.param_list = next(reader)
        file.close()

    def __parse_csv(self, user_name):
        file = open(self.file_path, 'r')
        reader = csv.reader(file)
        for row in reader:
            if row and self.__clean_str(row[0]) == self.__clean_str(user_name):
                self.data_user_list = row
        file.close()

        if len(self.data_user_list):
            self.__fill_user()
            return True

        return False

    def __fill_user(self):
        if self.__check_error():
            return

        for idx, param in enumerate(self.param_list):
            self.user[param] = self.data_user_list[idx]

    def __clean_str(self, str):
        return ' '.join(str.strip().lower().split())

    def find_user(self, user_name):
        if self.__parse_csv(user_name):
            print('Пользователь найден')
            return True
        else:
            print('Пользователь не найден')
            return False

    def get_param (self, param):
        if param in self.user:
            return self.user[param]

        self.__send_error(f"Параметр {param} отсутствует")
        return False

    def get_gender(self):
        gender = self.get_param('sex')
        if gender:
            return "женского" if gender.lower() == "female" else "мужского"

        self.__send_error('Параметр gender отсутствует')
        return False

    def get_device(self):
        device = self.get_param('device_type')
        if device:
            return "десктопного" if device.lower() == "desktop" else "мобильного"

        self.__send_error('Параметр device отсутствует ')
        return False

    def get_description(self):
        user_text = self.get_param('name') or 'без имени'
        browser_text = self.get_param('browser') or 'без имени'
        age_text = self.get_param('age') or 'с не указаным количеством'
        bill_text = self.get_param('bill') or 'не указанную сумму'
        region_text = self.get_param('region') or 'не указан'
        gender_text = self.get_gender() or 'без указаного'
        device_text = self.get_device() or 'не опознанного'
        return (
            f"Пользователь {user_text} {gender_text} пола, {age_text} лет совершил(а) покупку "
            f"на {bill_text} у.е. с {device_text} браузера {browser_text}. "
            f"Регион, из которого совершалась покупка: {region_text}."
        )

    def write_descriptions(self, output_file):
        with open(output_file, 'a') as file:
            file.write(self.get_description() + "\n")
        print(f'Пользователь добавлен в файл - {output_file}')



# 'Herman Miss. Alice' - для теста

if __name__ == "__main__":
    client = Client('web_clients_correct.csv')
    while True:
        print('Для выхода введите - q')
        user_name = input('Введите имя пользователя: ')
        if user_name.lower() == 'q':
            break
        elif client.find_user(user_name):
            client.write_descriptions('fined_web_clients.txt')