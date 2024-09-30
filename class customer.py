class Customer:
    def __init__(self, customer_id, first_name, address, phone_number):
        # Валидация всех полей через статические методы
        self.__customer_id = self.validate_customer_id(customer_id)
        self.__first_name = self.validate_first_name(first_name)
        self.__address = self.validate_address(address)
        self.__phone_number = self.validate_phone_number(phone_number)

    # Статические методы для валидации полей

    @staticmethod
    def validate_customer_id(customer_id):
        if isinstance(customer_id, int) and customer_id > 0:
            return customer_id
        else:
            raise ValueError("Customer ID must be a positive integer.")

    @staticmethod
    def validate_first_name(first_name):
        if isinstance(first_name, str) and len(first_name.strip()) > 0:
            return first_name.strip()
        else:
            raise ValueError("First name must be a non-empty string.")

    @staticmethod
    def validate_address(address):
        if isinstance(address, str) and len(address.strip()) > 0:
            return address.strip()
        else:
            raise ValueError("Address must be a non-empty string.")

    @staticmethod
    def validate_phone_number(phone_number):
        if isinstance(phone_number, str) and phone_number.isdigit() and len(phone_number) >= 10:
            return phone_number
        else:
            raise ValueError("Phone number must contain only digits and be at least 10 characters long.")

    # Геттеры для всех полей
    def get_customer_id(self):
        return self.__customer_id

    def get_first_name(self):
        return self.__first_name

    def get_address(self):
        return self.__address

    def get_phone_number(self):
        return self.__phone_number

    # Метод для вывода информации о клиенте
    def display_info(self):
        print(f"Customer ID: {self.__customer_id}")
        print(f"Name: {self.__first_name}")
        print(f"Address: {self.__address}")
        print(f"Phone: {self.__phone_number}")
