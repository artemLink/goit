contacts_book = {}


def input_error(func):
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except KeyError:
            return "Enter user name"
        except ValueError:
            return "Contact not found"
        except IndexError:
            return "Give me name and phone please"

    return wrapper


@input_error
def hello():
    return 'How can I help you?'


@input_error
def add_contact(contact):
    data = contact.split()
    contacts_book[data[1]] = data[2]
    return f'Add {data[1]} number: {data[2]}'


@input_error
def change_contact(contact):
    data = contact.split()
    contacts_book[data[1]] = data[2]
    return f'Change {data[1]} number: {data[2]}'


@input_error
def get_phone(data):
    if data not in contacts_book:
        return 'No contact in contact book'
    return f'Number: {contacts_book[data]}'


@input_error
def show_contacts():
    if not contacts_book:
        return "No contacts found"
    contact = 'Contacts\n'
    for name, number in contacts_book.items():
        contact += f'{name}: {number}'
    return contact


def main():
    while True:
        data = input('Enter command: ').lower()

        if 'hello' in data:
            print(hello())
        elif 'add' in data:
            print(add_contact(data))
        elif 'change' in data:
            print(change_contact(data))
        elif 'phone' in data:
            print(get_phone(data.split()[1]))
        elif 'show all' in data:
            print(show_contacts())
        elif any(keyword in data for keyword in ["good bye", "close", "exit"]):
            print("Good bye!")
            break
        else:
            print('Invalid command. Please try again.')


if __name__ == "__main__":
    main()
