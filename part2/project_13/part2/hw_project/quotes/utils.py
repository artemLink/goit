from pymongo import MongoClient


def get_mongodb():
    client = MongoClient('mongodb+srv://ravlykplus:qwerty1234@cluster0.hs7dfmm.mongodb.net/')
    db = client.hw_8
    return db
