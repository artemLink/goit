from AddressBook import AddressBook
from Table import BookTable, HelpTable
from Record import Record
from abc import ABC, abstractmethod, ABCMeta
from rich.console import Console
from decorators import input_error


handlers_dict = {}  # Глобальний словник для HandlerFactory
help_dict = {}  # Глобальний словник для таблиці HelpTable


class HandlerMeta(ABCMeta):
    def __new__(mcs, name, bases, nameplace):
        cls = super().__new__(mcs, name, bases, nameplace)
        if cls.__name__ != "Handler":
            handlers_dict[name.lower()] = cls()
            help_dict[name.lower()] = cls.__doc__
        return cls


class Handler(ABC, metaclass=HandlerMeta):
    @abstractmethod
    def handler(self):
        pass


class Hello(Handler):
    """Say hello!"""

    def handler(self):
        return print("Hello! I'm address book bot")


class Exit(Handler):
    """Exit from assistant"""

    def handler(self):
        return print("Good bye!")


class Show(Handler):
    """Show all contacts"""

    @input_error
    def handler(self):
        book = AddressBook()
        book.from_pickle()
        console = Console()
        show = BookTable(book.data)
        console.print(show.get_table())


class Create(Handler):
    """Create a new contacts record"""

    @input_error
    def handler(self):
        book = AddressBook()
        book.from_pickle()
        name = input("Input name>>> ")
        temp_obj = Record(name.lower())

        phone = input("Input phone>>> ")
        temp_obj.add_phone(phone)

        book.add_record(temp_obj)
        temp_obj = None

        book.to_pickle()


class Find(Handler):
    """Find contacts record by name"""

    @input_error
    def handler(self):
        book = AddressBook()
        book.from_pickle()
        request = input("Input request>>> ")
        console = Console()
        show = BookTable(book.find_to_show(request))
        console.print(show.get_table())


class AddPhone(Handler):
    """Add phone to the record"""

    @input_error
    def handler(self):
        book = AddressBook()
        book.from_pickle()

        name = input("Сontact name to add phone?>>> ")
        name.lower()
        obj_rec = book.find(name.capitalize())

        phone = input("Input phone>>> ")
        obj_rec.add_phone(phone)
        book.add_record(obj_rec)
        obj_rec = None
        book.to_pickle()


class AddBirthday(Handler):
    """Add contacts birthday to the record"""

    @input_error
    def handler(self):
        book = AddressBook()
        book.from_pickle()

        name = input("Сontact name to add birthday?>>> ")
        name.lower()
        obj_rec = book.find(name.capitalize())
        if obj_rec is not None:
            date = input("Input birthday (Year.Month.Day)>>> ")
            obj_rec.add_birthday(date)
            book.add_record(obj_rec)
            obj_rec = None
            book.to_pickle()


class DeleteContact(Handler):
    """Remove contacts record"""

    @input_error
    def handler(self):
        book = AddressBook()
        book.from_pickle()

        name = input("Сontact name to delete?>>> ")
        name.lower()
        book.delete(name.capitalize())
        book.to_pickle()


class Help(Handler):
    """Call command description"""

    def handler(self):
        console = Console()
        show = HelpTable(help_dict)
        console.print(show.get_table())


if __name__ == "__main__":
    print(handlers_dict)
    print(help_dict)
