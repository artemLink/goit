import django
import os
import pymongo
import sys
import datetime

sys.path.append(os.path.abspath('../'))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'quotes.settings')
django.setup()
from main.models import Author, Quote

mongo_client = pymongo.MongoClient('mongodb+srv://artemkislii90:8igGp5RMkUGvk1Hi@cluster0.2vfmeat.mongodb.net/')
mongo_db = mongo_client['homework']
mongo_authors = mongo_db['author']
mongo_quotes = mongo_db['quote'].find()

for author_data in mongo_authors.find():
    born_date = datetime.datetime.strptime(author_data['born_date'], "%B %d, %Y").strftime("%Y-%m-%d")
    author = Author.objects.create(
        fullname=author_data['fullname'],
        born_date=born_date,
        born_location=author_data['born_location'],
        description=author_data['description']
    )
    author.save()

for quote_data in mongo_quotes:
    # find author name from mongo
    author_name_mongo = mongo_authors.find_one({"_id": quote_data['author']})['fullname']
    # find author id in postgre
    author_id = Author.objects.get(fullname=author_name_mongo).id
    quote = Quote.objects.create(
        author_id=author_id,
        text=quote_data['text'],
        tags=quote_data['tags']
    )
    quote.save()

# Закриття підключення до MongoDB
mongo_client.close()
