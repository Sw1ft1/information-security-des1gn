import json
from typing import List, Dict, Any, Optional


class MyEntity:
    def __init__(self, customer_id: int, first_name: str, last_name: str, phone_number: str, inn: str, ogrn: str,
                 address: Optional[str] = None):
        self.customer_id = customer_id
        self.first_name = first_name
        self.last_name = last_name
        self.phone_number = phone_number
        self.inn = inn
        self.ogrn = ogrn
        self.address = address

    def to_dict(self) -> Dict[str, Any]:
        return {
            'customer_id': self.customer_id,
            'first_name': self.first_name,
            'last_name': self.last_name,
            'phone_number': self.phone_number,
            'inn': self.inn,
            'ogrn': self.ogrn,
            'address': self.address
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'MyEntity':
        return cls(**data)


class MyEntity_rep_json:
    def __init__(self, filename: str):
        self.filename = filename
        self.entities: List[MyEntity] = self.read_from_file()

    def read_from_file(self) -> List[MyEntity]:
        try:
            with open(self.filename, 'r') as file:
                data = json.load(file)
                return [MyEntity.from_dict(item) for item in data]
        except (FileNotFoundError, json.JSONDecodeError):
            return []

    def write_to_file(self) -> None:
        with open(self.filename, 'w') as file:
            json.dump([entity.to_dict() for entity in self.entities], file, indent=4)

    def get_by_id(self, customer_id: int) -> Optional[MyEntity]:
        for entity in self.entities:
            if entity.customer_id == customer_id:
                return entity
        return None

    def get_k_n_short_list(self, n: int, k: int) -> List[MyEntity]:
        return self.entities[n:n + k]

    def sort_entities(self, field: str) -> None:
        self.entities.sort(key=lambda x: getattr(x, field))

    def add_entity(self, entity: MyEntity) -> None:
        new_id = max((e.customer_id for e in self.entities), default=0) + 1
        entity.customer_id = new_id
        self.entities.append(entity)
        self.write_to_file()

    def replace_entity(self, customer_id: int, updated_entity: MyEntity) -> None:
        for i, entity in enumerate(self.entities):
            if entity.customer_id == customer_id:
                updated_entity.customer_id = customer_id
                self.entities[i] = updated_entity
                self.write_to_file()
                break

    def delete_entity(self, customer_id: int) -> None:
        self.entities = [entity for entity in self.entities if entity.customer_id != customer_id]
        self.write_to_file()

    def get_count(self) -> int:
        return len(self.entities)


# Пример использования
if __name__ == "__main__":
    repository = MyEntity_rep_json("customers.json")

    # Добавление нового объекта
    new_entity = MyEntity(customer_id=0, first_name="Иван", last_name="Иванов", phone_number="1234567890",
                          inn="123456789012", ogrn="1234567890123", address="Москва")
    repository.add_entity(new_entity)

    # Получение количества объектов
    print("Количество объектов:", repository.get_count())

    # Получение объекта по ID
    entity = repository.get_by_id(1)
    if entity:
        print("Найден объект:", entity.to_dict())

    # Получение второго по счету 20 объектов
    short_list = repository.get_k_n_short_list(20, 20)
    print("Вторые 20 объектов:", [e.to_dict() for e in short_list])

    # Сортировка по фамилии
    repository.sort_entities("last_name")

    # Удаление объекта
    repository.delete_entity(1)
