from mongoengine import connect
from models import Quote, Author


connect(host='mongodb+srv://artemkislii90:8igGp5RMkUGvk1Hi@cluster0.2vfmeat.mongodb.net/', db='homework')


def search_quotes(command):
    command = command.strip()
    parts = command.split(':')

    if len(parts) != 2:
        print("Некоректний формат команди.")
        return

    key, value = parts
    key = key.lower().strip()
    value = value.strip()

    if key == 'name':
        author = Author.objects(fullname=value).first()
        if author:
            quotes = Quote.objects(author=author)
        else:
            print(f"Автор з ім'ям '{value}' не знайдений.")
            return
    elif key == 'tag':
        quotes = Quote.objects(tags=value)
    elif key == 'tags':
        tags = value.split(',')
        quotes = Quote.objects(tags__in=tags)
    else:
        print("Невідома команда.")
        return

    for quote in quotes:
        print(quote.quote)


# Нескінченний цикл для прийому команд
while True:
    command = input("Введіть команду (наприклад, name: Steve Martin): ")
    if command.lower() == 'exit':
        break
    search_quotes(command)
