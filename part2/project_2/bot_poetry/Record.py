from Field import Name, Phone, Birthday
from datetime import date
from decorators import input_error


class Record:
    def __init__(self, name: str):
        self.name = Name(name)
        self.phones = []
        self.birthdays = ""

    def __str__(self):
        return f"Name: {self.name}\nPhones: {', '.join(p.get_value for p in self.phones)}\nBirthday: {self.birthdays}"

    # повертає кількість днів до наступного дня народження
    @input_error
    def days_to_birthday(self):
        if self.birthdays:
            today = date.today()
            birhtday = self.birthdays.get_value
            if today.month > birhtday.month:
                result = birhtday.replace(year=today.year + 1) - today
                # print(f"{self.name}'s birthday in {result.days} days")
                return result.days
            else:
                result = birhtday.replace(year=today.year) - today
                # print(f"{self.name}'s birthday in {result.days} days")
                return result.days
        else:
            # print(f"{self.name}'s birthday has not been added")
            return False

    # метод додавання дня народження
    @input_error
    def add_birthday(self, input_date: str):
        self.birthdays = Birthday(input_date)
        print(f"Birthday of {self.name} is already added.")

    # метод додавання телефону
    @input_error
    def add_phone(self, input_phone: str):
        phone = Phone(input_phone)
        if phone.get_value not in [p.get_value for p in self.phones]:
            self.phones.append(phone)
            print(f"{phone} successfully added.")
        else:
            return f"{phone} is already exists."

    # видаляє телефон, або виводить, що немає номеру в всписку
    @input_error
    def remove_phone(self, phone: str):
        if phone in [p.get_value for p in self.phones]:
            self.phones.remove(
                self.phones[[p.get_value for p in self.phones].index(phone)]
            )
            print(f"{phone} successfully removed")
        else:
            print(f"{phone} not found in the list of phones.")

    # редагує номер
    @input_error
    def edit_phone(self, old_phone, new_phone):
        phone = Phone(new_phone)
        if old_phone in [p.get_value for p in self.phones]:
            position = [p.get_value for p in self.phones].index(old_phone)
            self.phones.remove(self.phones[position])
            self.phones.insert(position, phone)
            print(f"{phone} successfully adited.")
        else:
            print(f"{phone} not found in the list of phones.")

    # пошук номеру телефону
    @input_error
    def find_phone(self, phone):
        phone = Phone(phone)
        if phone.value in [p.get_value for p in self.phones]:
            print(f"{self.name.get_value}: {phone}")
        else:
            print(f"{phone} not in {self.name.get_value} contacts")
