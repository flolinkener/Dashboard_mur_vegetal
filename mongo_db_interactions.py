import pymongo
import datetime
import random
import time
import json
#connects to the db and to the right collection
client = pymongo.MongoClient('localhost', 27017)
db = client.green_wall
collection = db.data

#get the latest entry of the database based on timestamp
def fetch_data(data):
    cursor = collection.find({}).sort([('timestamp', -1)]).limit(1) #good sort
    for document in cursor:
        return document[data]

#get the latest entry of the database based on timestamp
def fetch_data_from_id(data,id):    

    cursor = collection.find({"id": id}).sort([('timestamp', -1)]).limit(1) #good sort
    for document in cursor:
        return document[data]

#write a new document in the database
def write_data(id,temperature, humidity, battery):
    post = {"timestamp": datetime.datetime.now(),
        "id": id,
        "temperature": temperature,
        "humidity": humidity,
        "battery": battery
    }
    collection.insert_one(post).inserted_id
    return 0