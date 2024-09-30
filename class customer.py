class Customer:
    def __init__(self, customer_id, first_name, address, phone_number):
        self.__customer_id = customer_id
        self.__first_name = first_name
        self.__address = address
        self.__phone_number = phone_number

    # Геттеры и сеттеры для customer_id
    def get_customer_id(self):
        return self.__customer_id

    def set_customer_id(self, customer_id):
        self.__customer_id = customer_id

    # Геттеры и сеттеры для first_name
    def get_first_name(self):
        return self.__first_name

    def set_first_name(self, first_name):
        self.__first_name = first_name

    # Геттеры и сеттеры для address
    def get_address(self):
        return self.__address

    def set_address(self, address):
        self.__address = address

    # Геттеры и сеттеры для phone_number
    def get_phone_number(self):
        return self.__phone_number

    def set_phone_number(self, phone_number):
        self.__phone_number = phone_number

    # Метод для вывода информации о клиенте
    def display_info(self):
        print(f"Customer ID: {self.__customer_id}")
        print(f"Name: {self.__first_name}")
        print(f"Address: {self.__address}")
        print(f"Phone: {self.__phone_number}")
