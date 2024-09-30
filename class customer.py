class CustomerBase:
    def __init__(self, customer_id, first_name, last_name, phone_number, inn=None, ogrn=None):
        self.customer_id = customer_id
        self.first_name = first_name
        self.last_name = last_name
        self.phone_number = phone_number
        self.inn = inn
        self.ogrn = ogrn

    def __repr__(self):
        return (f"{self.__class__.__name__}(customer_id={self.customer_id}, "
                f"first_name='{self.first_name}', last_name='{self.last_name}', "
                f"phone_number='{self.phone_number}', inn='{self.inn}', ogrn='{self.ogrn}')")

    def __eq__(self, other):
        if isinstance(other, CustomerBase):
            return (self.customer_id == other.customer_id and
                    self.first_name == other.first_name and
                    self.last_name == other.last_name and
                    self.phone_number == other.phone_number)
        return False

    def __str__(self):
        return f"{self.first_name} {self.last_name} (ID: {self.customer_id})"


class Customer(CustomerBase):
    def __init__(self, customer_id, first_name, last_name, address, phone_number, inn=None, ogrn=None):
        super().__init__(customer_id, first_name, last_name, phone_number, inn, ogrn)
        self.address = address

    def __repr__(self):
        base_repr = super().__repr__()
        return f"{base_repr[:-1]}, address='{self.address}')"

    def __str__(self):
        return f"Customer: {self.first_name} {self.last_name}, Address: {self.address}, Phone: {self.phone_number}"


class CustomerShort(CustomerBase):
    def __init__(self, customer):
        if isinstance(customer, CustomerBase):
            # Вызов конструктора базового класса
            super().__init__(customer.customer_id, customer.first_name, customer.last_name,
                             customer.phone_number, customer.inn, customer.ogrn)
        else:
            raise ValueError("Invalid Customer object passed.")

    def __str__(self):
        # Формирование краткой версии: Фамилия и инициалы
        return f"{self.last_name} {self.first_name[0]}. (Phone: {self.phone_number}, INN: {self.inn}, OGRN: {self.ogrn})"

# Создание объекта полной версии Customer
customer = Customer(1, "John", "Doe", "123 Main St", "1234567890", inn="123456789", ogrn="987654321")

# Создание объекта краткой версии CustomerShort
short_customer = CustomerShort(customer)

# Вывод полной версии объекта
print(customer)  # Output: Customer: John Doe, Address: 123 Main St, Phone: 1234567890

# Вывод краткой версии объекта
print(short_customer)  # Output: Doe J. (Phone: 1234567890, INN: 123456789, OGRN: 987654321)

# Сравнение объектов
print(customer == short_customer)  # Output: True (по базовым полям)
