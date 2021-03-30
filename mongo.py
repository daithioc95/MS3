import os
import pymongo
import json
if os.path.exists("env.py"):
    import env
MONGO_URI = os.environ.get("MONGO_URI")
DATABASE = "ms3_quotes"
COLLECTION = "quotes"
def mongo_connect(url):
    try:
        conn = pymongo.MongoClient(url)
        print("Mongo is connected")
        return conn
    except pymongo.errors.ConnectionFailure as e:
        print("Could not connect to MongoDB: %s") % e
conn = mongo_connect(MONGO_URI)
coll = conn[DATABASE][COLLECTION]
documents = coll.find()

# Upload quotes from data.txt to quotes collection

# with open('data.txt') as json_file:
#     data = json.load(json_file)
#     for p in data:
#         coll.insert_one(p)

# coll.ensureIndex( { "Quote":1 }, { unique:true, dropDups:true } )
