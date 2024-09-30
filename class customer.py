import json

class Customer:
    def __init__(self, customer_id=None, first_name=None, address=None, phone_number=None):
        # Основной конструктор с валидацией
        self.customer_id = customer_id
        self.first_name = first_name
        self.address = address
        self.phone_number = phone_number

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

    # Свойства для customer_id
    @property
    def customer_id(self):
        return self.__customer_id

    @customer_id.setter
    def customer_id(self, value):
        self.__customer_id = self.validate_customer_id(value)

    # Свойства для first_name
    @property
    def first_name(self):
        return self.__first_name

    @first_name.setter
    def first_name(self, value):
        self.__first_name = self.validate_first_name(value)

    # Свойства для address
    @property
    def address(self):
        return self.__address

    @address.setter
    def address(self, value):
        self.__address = self.validate_address(value)

    # Свойства для phone_number
    @property
    def phone_number(self):
        return self.__phone_number

    @phone_number.setter
    def phone_number(self, value):
        self.__phone_number = self.validate_phone_number(value)

    # Альтернативный конструктор из строки
    @classmethod
    def from_string(cls, customer_str):
        try:
            customer_id, first_name, address, phone_number = customer_str.split(',')
            return cls(
                customer_id=int(customer_id.strip()),
                first_name=first_name.strip(),
                address=address.strip(),
                phone_number=phone_number.strip()
            )
        except ValueError as e:
            raise ValueError(f"Error parsing string: {e}")

    # Альтернативный конструктор из JSON
    @classmethod
    def from_json(cls, json_str):
        try:
            data = json.loads(json_str)
            return cls(
                customer_id=data['customer_id'],
                first_name=data['first_name'],
                address=data['address'],
                phone_number=data['phone_number']
            )
        except (KeyError, json.JSONDecodeError) as e:
            raise ValueError(f"Error parsing JSON: {e}")

    # Полная версия объекта (информативная)
    def __repr__(self):
        return (f"Customer(customer_id={self.customer_id}, first_name='{self.first_name}', "
                f"address='{self.address}', phone_number='{self.phone_number}')")

    # Краткая версия объекта (для простого вывода)
    def __str__(self):
        return f"Customer: {self.first_name} (ID: {self.customer_id})"

    # Метод для сравнения объектов на равенство
    def __eq__(self, other):
        if isinstance(other, Customer):
            return (self.customer_id == other.customer_id and
                    self.first_name == other.first_name and
                    self.address == other.address and
                    self.phone_number == other.phone_number)
        return False

    # Метод для вывода полной информации о клиенте
    def display_info(self):
        print(f"Customer ID: {self.customer_id}")
        print(f"Name: {self.first_name}")
        print(f"Address: {self.address}")
        print(f"Phone: {self.phone_number}")
