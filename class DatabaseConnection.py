from typing import Optional, List
import sqlite3

# Интерфейс репозитория
class IRepository:
    def get_by_id(self, id: int):
        raise NotImplementedError

    def get_all(self) -> List:
        raise NotImplementedError

    def add(self, entity):
        raise NotImplementedError

    def update(self, id: int, entity):
        raise NotImplementedError

    def delete(self, id: int):
        raise NotImplementedError


# Сущность MyEntity
class MyEntity:
    def __init__(self, customer_id: int, first_name: str, last_name: str, phone_number: str, inn: str, ogrn: str, address: Optional[str] = None):
        self.customer_id = customer_id
        self.first_name = first_name
        self.last_name = last_name
        self.phone_number = phone_number
        self.inn = inn
        self.ogrn = ogrn
        self.address = address

    def to_dict(self) -> dict:
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
    def from_dict(cls, data: dict) -> 'MyEntity':
        return cls(**data)


# Соединение с базой данных
class DatabaseConnection:
    _instance = None

    def __new__(cls, db_file: str):
        if cls._instance is None:
            cls._instance = super(DatabaseConnection, cls).__new__(cls)
            cls._instance.connection = sqlite3.connect(db_file)
        return cls._instance

    def close(self):
        if self.connection:
            self.connection.close()

    def get_connection(self):
        return self.connection


# Репозиторий MyEntity_rep_DB
class MyEntity_rep_DB:
    def __init__(self):
        self.db_connection = DatabaseConnection("my_entities.db")
        self.create_table()

    def create_table(self):
        with self.db_connection.get_connection() as conn:
            conn.execute('''
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
        cursor = self.db_connection.get_connection().cursor()
        cursor.execute("SELECT * FROM MyEntities WHERE customer_id = ?", (customer_id,))
        row = cursor.fetchone()
        if row:
            return MyEntity(*row)
        return None

    def get_k_n_short_list(self, n: int, k: int) -> List[MyEntity]:
        cursor = self.db_connection.get_connection().cursor()
        cursor.execute("SELECT * FROM MyEntities LIMIT ? OFFSET ?", (k, n))
        rows = cursor.fetchall()
        return [MyEntity(*row) for row in rows]

    def add_entity(self, entity: MyEntity) -> None:
        with self.db_connection.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('''
                INSERT INTO MyEntities (first_name, last_name, phone_number, inn, ogrn, address)
                VALUES (?, ?, ?, ?, ?, ?)
            ''', (entity.first_name, entity.last_name, entity.phone_number, entity.inn, entity.ogrn, entity.address))
            entity.customer_id = cursor.lastrowid

    def replace_entity(self, customer_id: int, updated_entity: MyEntity) -> None:
        with self.db_connection.get_connection() as conn:
            conn.execute('''
                UPDATE MyEntities
                SET first_name = ?, last_name = ?, phone_number = ?, inn = ?, ogrn = ?, address = ?
                WHERE customer_id = ?
            ''', (updated_entity.first_name, updated_entity.last_name, updated_entity.phone_number,
                  updated_entity.inn, updated_entity.ogrn, updated_entity.address, customer_id))

    def delete_entity(self, customer_id: int) -> None:
        with self.db_connection.get_connection() as conn:
            conn.execute('DELETE FROM MyEntities WHERE customer_id = ?', (customer_id,))

    def get_count(self) -> int:
        cursor = self.db_connection.get_connection().cursor()
        cursor.execute("SELECT COUNT(*) FROM MyEntities")
        return cursor.fetchone()[0]


# Адаптер
class RepositoryAdapter(IRepository):
    def __init__(self, adaptee: MyEntity_rep_DB):
        self.adaptee = adaptee

    def get_by_id(self, id: int):
        return self.adaptee.get_by_id(id)

    def get_all(self) -> List[MyEntity]:
        count = self.adaptee.get_count()
        return self.adaptee.get_k_n_short_list(0, count)

    def add(self, entity: MyEntity):
        self.adaptee.add_entity(entity)

    def update(self, id: int, entity: MyEntity):
        self.adaptee.replace_entity(id, entity)

    def delete(self, id: int):
        self.adaptee.delete_entity(id)


# Пример использования
if __name__ == "__main__":
    # Создаем оригинальный репозиторий
    db_repository = MyEntity_rep_DB()

    # Адаптируем через RepositoryAdapter
    adapter = RepositoryAdapter(db_repository)

    # Добавление новой сущности
    new_entity = MyEntity(customer_id=0, first_name="John", last_name="Doe", phone_number="123456789", inn="123456789012", ogrn="1234567890123")
    adapter.add(new_entity)

    # Получение всех сущностей
    all_entities = adapter.get_all()
    for entity in all_entities:
        print(entity.to_dict())

    # Получение сущности по ID
    entity = adapter.get_by_id(1)
    print(entity.to_dict() if entity else "Entity not found")

    # Удаление сущности
    adapter.delete(1)

    # Закрытие соединения
    DatabaseConnection._instance.close()
