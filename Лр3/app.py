import tkinter as tk
from tkinter import ttk, messagebox
from typing import List


# --- Паттерн "Наблюдатель" ---
class Observer:
    def update(self, data):
        raise NotImplementedError


class Observable:
    def __init__(self):
        self._observers: List[Observer] = []

    def add_observer(self, observer: Observer):
        if observer not in self._observers:
            self._observers.append(observer)

    def remove_observer(self, observer: Observer):
        if observer in self._observers:
            self._observers.remove(observer)

    def notify_observers(self, data):
        for observer in self._observers:
            observer.update(data)


# --- Сущность ---
class Supplier:
    def __init__(self, supplier_id: int, name: str, address: str, phone: str):
        self.supplier_id = supplier_id
        self.name = name
        self.address = address
        self.phone = phone

    def to_dict(self) -> dict:
        return {
            "supplier_id": self.supplier_id,
            "name": self.name,
            "address": self.address,
            "phone": self.phone,
        }


# --- Репозиторий ---
class ObservableRepository(Observable):
    def __init__(self):
        super().__init__()
        self.suppliers: List[Supplier] = []

    def add_supplier(self, supplier: Supplier):
        self.suppliers.append(supplier)
        self.notify_observers(self.suppliers)

    def delete_supplier(self, supplier_id: int):
        self.suppliers = [s for s in self.suppliers if s.supplier_id != supplier_id]
        self.notify_observers(self.suppliers)

    def get_all_suppliers(self):
        return self.suppliers

    def sort_suppliers(self, key: str, reverse: bool = False):
        if key == "ID":
            self.suppliers.sort(key=lambda s: s.supplier_id, reverse=reverse)
        elif key == "Name":
            self.suppliers.sort(key=lambda s: s.name.lower(), reverse=reverse)
        elif key == "Address":
            self.suppliers.sort(key=lambda s: s.address.lower(), reverse=reverse)
        elif key == "Phone":
            self.suppliers.sort(key=lambda s: s.phone, reverse=reverse)
        self.notify_observers(self.suppliers)


# --- Контроллер главного окна ---
class MainController:
    def __init__(self, repository: ObservableRepository):
        self.repository = repository

    def get_all_suppliers(self):
        return self.repository.get_all_suppliers()

    def delete_supplier(self, supplier_id: int):
        self.repository.delete_supplier(supplier_id)

    def sort_suppliers(self, key: str, reverse: bool = False):
        self.repository.sort_suppliers(key, reverse)


# --- Контроллер окна добавления ---
class AddSupplierController:
    def __init__(self, repository: ObservableRepository):
        self.repository = repository

    def add_supplier(self, name: str, address: str, phone: str):
        supplier_id = len(self.repository.suppliers) + 1  # Генерация ID
        supplier = Supplier(supplier_id, name, address, phone)
        self.repository.add_supplier(supplier)


# --- Главное окно ---
class MainWindow(tk.Tk, Observer):
    def __init__(self, controller: MainController):
        super().__init__()
        self.title("Supplier Management")
        self.geometry("700x400")

        # Контроллер
        self.controller = controller

        # Таблица
        self.tree = ttk.Treeview(self, columns=("ID", "Name", "Address", "Phone"), show="headings")
        for col in self.tree["columns"]:
            self.tree.heading(col, text=col, command=lambda c=col: self.sort_table(c))
        self.tree.pack(fill=tk.BOTH, expand=True)

        # Панель управления
        self.control_frame = ttk.Frame(self)
        self.control_frame.pack(fill=tk.X, padx=10, pady=5)

        ttk.Button(self.control_frame, text="Add Supplier", command=self.open_add_supplier_window).pack(side=tk.LEFT, padx=5)
        ttk.Button(self.control_frame, text="Delete Selected", command=self.delete_selected_supplier).pack(side=tk.LEFT, padx=5)

        # Подписываемся как наблюдатель
        self.controller.repository.add_observer(self)

        # Параметры сортировки
        self.sort_reverse = False

    def open_add_supplier_window(self):
        # Передаем только контроллер AddSupplierController
        AddSupplierWindow(AddSupplierController(self.controller.repository))

    def delete_selected_supplier(self):
        selected_item = self.tree.selection()
        if not selected_item:
            messagebox.showerror("Error", "No supplier selected!")
            return

        supplier_id = int(self.tree.item(selected_item)["values"][0])
        self.controller.delete_supplier(supplier_id)

    def sort_table(self, column: str):
        self.sort_reverse = not self.sort_reverse  # Переключение порядка сортировки
        self.controller.sort_suppliers(key=column, reverse=self.sort_reverse)

    def update(self, data):
        # Обновление таблицы
        for row in self.tree.get_children():
            self.tree.delete(row)
        for supplier in data:
            self.tree.insert(
                "",
                tk.END,
                values=(supplier.supplier_id, supplier.name, supplier.address, supplier.phone),
            )


# --- Окно добавления поставщика ---
class AddSupplierWindow(tk.Toplevel):
    def __init__(self, controller: AddSupplierController):
        super().__init__()
        self.title("Add Supplier")
        self.geometry("400x200")
        self.controller = controller

        # Поля ввода
        self.name_var = tk.StringVar()
        self.address_var = tk.StringVar()
        self.phone_var = tk.StringVar()

        ttk.Label(self, text="Name:").grid(row=0, column=0, padx=5, pady=5, sticky=tk.W)
        ttk.Entry(self, textvariable=self.name_var).grid(row=0, column=1, padx=5, pady=5)

        ttk.Label(self, text="Address:").grid(row=1, column=0, padx=5, pady=5, sticky=tk.W)
        ttk.Entry(self, textvariable=self.address_var).grid(row=1, column=1, padx=5, pady=5)

        ttk.Label(self, text="Phone:").grid(row=2, column=0, padx=5, pady=5, sticky=tk.W)
        ttk.Entry(self, textvariable=self.phone_var).grid(row=2, column=1, padx=5, pady=5)

        ttk.Button(self, text="Add", command=self.add_supplier).grid(row=3, column=0, columnspan=2, pady=10)

    def add_supplier(self):
        name = self.name_var.get()
        address = self.address_var.get()
        phone = self.phone_var.get()

        # Валидация данных
        if not name or not address or not phone:
            messagebox.showerror("Error", "All fields are required!")
            return

        if not phone.isdigit():
            messagebox.showerror("Error", "Phone must be numeric!")
            return

        self.controller.add_supplier(name, address, phone)
        self.destroy()


# --- Запуск приложения ---
if __name__ == "__main__":
    repository = ObservableRepository()
    main_controller = MainController(repository)
    app = MainWindow(main_controller)
    app.mainloop()
