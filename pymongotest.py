import json
import pymongo
from pymongo import MongoClient

client = MongoClient('localhost', 27017)

mydb = client["mydatabase"]
collection_song = mydb["songs"]

with open('test.json') as f:
    file_data = json.load(f)

collection_song.insert_one(file_data)

for x in collection_song.find():
  print(x)
    # 192.168.1.51