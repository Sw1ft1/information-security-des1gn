import sqlite3  # Используется только для демонстрации структуры; замените на другую базу данных
from typing import List, Dict, Any, Optional

class MyEntity:
    def __init__(self, customer_id: int, first_name: str, last_name: str, phone_number: str, inn: str, ogrn: str, address: Optional[str] = None):
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


class MyEntity_rep_DB:
    def __init__(self, db_file: str):
        self.connection = sqlite3.connect(db_file)
        self.create_table()

    def create_table(self):
        with self.connection:
            self.connection.execute('''
                CREATE TABLE IF NOT EXISTS MyEntities (
                    customer_id INTEGER PRIMARY KEY AUTOINCREMENT,
                    first_name TEXT NOT NULL,
                    last_name TEXT NOT NULL,
                    phone_number TEXT NOT NULL,
                    inn TEXT NOT NULL,
                    ogrn TEXT NOT NULL,
                    address TEXT
                )
            ''')

    def get_by_id(self, customer_id: int) -> Optional[MyEntity]:
        cursor = self.connection.cursor()
        cursor.execute("SELECT * FROM MyEntities WHERE customer_id = ?", (customer_id,))
        row = cursor.fetchone()
        if row:
            return MyEntity(*row)
        return None

    def get_k_n_short_list(self, n: int, k: int) -> List[MyEntity]:
        cursor = self.connection.cursor()
        cursor.execute("SELECT * FROM MyEntities LIMIT ? OFFSET ?", (k, n))
        rows = cursor.fetchall()
        return [MyEntity(*row) for row in rows]

    def add_entity(self, entity: MyEntity) -> None:
        with self.connection:
            cursor = self.connection.cursor()
            cursor.execute('''
                INSERT INTO MyEntities (first_name, last_name, phone_number, inn, ogrn, address)
                VALUES (?, ?, ?, ?, ?, ?)
            ''', (entity.first_name, entity.last_name, entity.phone_number, entity.inn, entity.ogrn, entity.address))
            entity.customer_id = cursor.lastrowid  # Обновляем ID сущности

    def replace_entity(self, customer_id: int, updated_entity: MyEntity) -> None:
        with self.connection:
            self.connection.execute('''
                UPDATE MyEntities
                SET first_name = ?, last_name = ?, phone_number = ?, inn = ?, ogrn = ?, address = ?
                WHERE customer_id = ?
            ''', (updated_entity.first_name, updated_entity.last_name, updated_entity.phone_number, updated_entity.inn, updated_entity.ogrn, updated_entity.address, customer_id))

    def delete_entity(self, customer_id: int) -> None:
        with self.connection:
            self.connection.execute('DELETE FROM MyEntities WHERE customer_id = ?', (customer_id,))

    def get_count(self) -> int:
        cursor = self.connection.cursor()
        cursor.execute("SELECT COUNT(*) FROM MyEntities")
        return cursor.fetchone()[0]

    def close(self):
        self.connection.close()


# Пример использования
if __name__ == "__main__":
    db_repository = MyEntity_rep_DB("my_entities.db")

    # Добавление новой сущности
    new_entity = MyEntity(customer_id=0, first_name="John", last_name="Doe", phone_number="123456789", inn="123456789012", ogrn="1234567890123")
    db_repository.add_entity(new_entity)

    # Получение сущности по ID
    entity = db_repository.get_by_id(1)
    print(entity.to_dict() if entity else "Entity not found")

    # Получение количества сущностей
    count = db_repository.get_count()
    print(f"Total entities: {count}")

    # Закрытие соединения
    db_repository.close()
