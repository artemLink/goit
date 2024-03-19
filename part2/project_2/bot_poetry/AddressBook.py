from collections import UserDict
from Record import Record
import pickle
import re
from decorators import input_error


class AddressBook(UserDict):
    # додає запис до адресної книги
    @input_error
    def add_record(self, record: Record):
        self.data[record.name.get_value] = record
        print(f"Сontact {record.name.get_value} has been added to the records")

    # знаходить за ім'ям.
    @input_error
    def find(self, name):
        if name in self.data.keys():
            return self.data[name]
        else:
            print(f"{name} not found")
            return None

    # видаляє запис за ім'ям.
    @input_error
    def delete(self, name):
        if name in self.data.keys():
            del self.data[name]
            print(f"{name} is delete")
        else:
            print(f"{name} not found")

    # повертає генератор за записами;
    # якщо кількість контактів запиту більша за кількість контактів в словнику -> всі контакти;
    @input_error
    def iterator(self, quantity):
        counter = 0
        result = ""
        if len(self.data) < quantity:
            for record in self.data.values():
                result += f"\n{record}"
            yield result
        else:
            for record in self.data.values():
                result += f"\n{record}"
                counter += 1
                if counter >= quantity:
                    yield result
                    counter = 0
                    result = ""
            if counter > 0:
                yield result

    # серіалізація даних адресної книги
    @input_error
    def to_pickle(self, file_name="backup_address_book"):
        with open(f"{file_name}.pkl", "wb") as file:
            pickle.dump(self.data, file)
        print(f"Address book saved to {file_name}.pkl")

    # десеріалізація даних адресної книги
    @input_error
    def from_pickle(self, filename="backup_address_book"):
        try:
            with open(f"{filename}.pkl", "rb") as file:
                data = pickle.load(file)
                self.data.update(data)
            print(f"Address book loaded from {filename}")

        except FileNotFoundError:
            print(f"File {filename} not found. Creating a new address book.")

    # пошук одного або кількох користувачів
    # за кількома цифрами номера телефону або літерами імені
    @input_error
    def find_to_show(self, find_str: str):
        find_dict = {}
        for name, contact in self.data.items():
            if re.search(find_str, str(name.lower())):
                find_dict[name] = contact
        if len(find_dict) > 0:
            return find_dict
        else:
            print(f"{find_str} not found")
