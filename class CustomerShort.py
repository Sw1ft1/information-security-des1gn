class CustomerShort:
    def __init__(self, customer):
        # Инициализация краткой версии на основе исходного класса
        if isinstance(customer, Customer):
            self.full_name = f"{customer.last_name} {customer.first_name[0]}."
            self.phone_number = customer.phone_number
            self.inn = customer.inn if customer.inn else "ИНН не указан"
            self.ogrn = customer.ogrn if customer.ogrn else "ОГРН не указан"
        else:
            raise ValueError("Invalid Customer object passed.")

    def __repr__(self):
        return (f"CustomerShort(full_name='{self.full_name}', phone_number='{self.phone_number}', "
                f"inn='{self.inn}', ogrn='{self.ogrn}')")

    def __str__(self):
        return f"{self.full_name}, телефон: {self.phone_number}, ИНН: {self.inn}, ОГРН: {self.ogrn}"
