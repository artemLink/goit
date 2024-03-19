from datetime import datetime
from abc import ABC, abstractmethod


class Field(ABC):
    @abstractmethod
    def __str__(self):
        pass


class Name(Field):
    def __init__(self, name):
        self.__name = None
        self.set_value = name

    @property
    def get_value(self):
        return self.__name

    @get_value.setter
    def set_value(self, value: str):
        if len(value) > 0:
            self.__name = value.capitalize()
        else:
            print(f"Name {value} isn't correct.")
            raise ValueError

    def __str__(self):
        return f"{self.get_value}"


class Phone(Field):
    def __init__(self, phone):
        self.__phone = None
        self.set_value = phone

    @property
    def get_value(self):
        return self.__phone

    @get_value.setter
    def set_value(self, value: str):
        if len(value) == 10 and value.isdigit():
            self.__phone = value
        else:
            print((f"Phone {value} isn't valid"))
            raise ValueError

    def __str__(self):
        return f"{self.get_value}"


class Birthday(Field):
    def __init__(self, birthday):
        self.__birthday = None
        self.set_value = birthday

    @property
    def get_value(self):
        return self.__birthday

    @get_value.setter
    def set_value(self, value: str):
        if (
            len(value.split(".")) == 3
            and all(part.isdigit() for part in value.split("."))
            and len(value.split(".")[0]) == 4
        ):
            self.__birthday = datetime.strptime(value, "%Y.%m.%d").date()
        else:
            print("Date format isn't valid, should be: year.month.day")
            raise ValueError

    def __str__(self):
        return f"{self.get_value}"
