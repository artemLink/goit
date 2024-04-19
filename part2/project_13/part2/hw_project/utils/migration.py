import os

import django
from pymongo import MongoClient


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'hw_project.settings')
django.setup()

from quotes.models import Quote, Tag, Author  # noqa

client = MongoClient('mongodb+srv://ravlykplus:qwerty1234@cluster0.hs7dfmm.mongodb.net/')

db = client.hw_8

# Заповнення таблиці quotes_author
authors = db.authors.find()

for author in authors:
    Author.objects.get_or_create(
        fullname=author['fullname'],
        born_date=author['born_date'],
        born_location=author['born_location'],
        description=author['description'],
    )

# Заповнення таблиць:
quotes = db.quotes.find()

for quote in quotes:
    tags = []
    for tag in quote['tags']:

        # quotes_tag
        t, *_ = Tag.objects.get_or_create(name=tag)
        tags.append(t)

    exist_quote = bool(len(Quote.objects.filter(quote=quote['quote'])))

    if not exist_quote:
        author = db.authors.find_one({'_id': quote['author']})
        a = Author.objects.get(fullname=author['fullname'])

        # quotes_quote
        q = Quote.objects.create(
            quote=quote['quote'],
            author=a,
        )

        # quotes_quote_tags
        for tag in tags:
            q.tags.add(tag)



