from mongoengine import connect
import json
from models import Quote, Author


with open('authors.json', 'r') as file:
    authors_data = json.load(file)


connect(host='mongodb+srv://artemkislii90:8igGp5RMkUGvk1Hi@cluster0.2vfmeat.mongodb.net/', db='homework')


for author_data in authors_data:
    author = Author(**author_data)
    author.save()

with open('quotes.json', 'r') as file:
    quotes_data = json.load(file)

author_id_map = {author.fullname: author.id for author in Author.objects}

for quote_data in quotes_data:

    author_name = quote_data['author']
    author_id = author_id_map.get(author_name)
    if author_id:
        quote_data['author'] = str(author_id)
    else:
        print(f"Author '{author_name}' not found in database.")

for quote_data in quotes_data:
    quote = Quote(**quote_data)
    quote.save()
