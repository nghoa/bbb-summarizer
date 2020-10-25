from pymongo import MongoClient
from pprint import pprint

client = MongoClient('mongodb://127.0.1.1:27017/')
dbs = client.list_database_names()
db = client['local'].list_collection_names()
db = client['local']
collection = db['me']

print(collection)