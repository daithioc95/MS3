import os
import pymongo
import json
if os.path.exists("env.py"):
    import env
MONGO_URI = os.environ.get("MONGO_URI")
DATABASE = "ms3_quotes"
COLLECTION_QUTOES = "quotes"
COLLECTION_AUTHORS = "authors"
def mongo_connect(url):
    try:
        conn = pymongo.MongoClient(url)
        print("Mongo is connected")
        return conn
    except pymongo.errors.ConnectionFailure as e:
        print("Could not connect to MongoDB: %s") % e
conn = mongo_connect(MONGO_URI)
coll1 = conn[DATABASE][COLLECTION_QUTOES]
coll2 = conn[DATABASE][COLLECTION_AUTHORS]


documents_authors = coll1.find({},{ "_id": 0, "Author": 1})
# documents = coll1

# *** Delete all documents
coll1.delete_many({})

# ***Adding category to entire list
# with open('data.txt') as json_file:
#     data = json.load(json_file)
#     store_list = []
#     for p in data:
#         p['Book'] = ''
#         store_list.append(p)
#         # print(p)
# with open('data_copy.txt', 'w') as filehandle:
#     json.dump(store_list, filehandle)
#     # p.add({"Book":"None"})

# ****To split and update the Author and Books fields
# for doc in documents_authors:
#     k = doc["Author"].split(",")
#     # print(k[0])
#     # coll1.update({"Author":doc},{"$set": {"Author": k[0]}})
#     try:
#         coll1.replaceone({"Author": doc["Author"]}, {"Author": k[0], "Book": k[1]})
#         # coll1.update({"Author":doc},{"$set": {"Book": k[1]}})
#     except:
#         coll1.replaceone({"Author": doc["Author"]}, {"Author": k[0], "Book": "None"})
#     print(coll1.find())

# Upload quotes from data.txt to quotes collection

# *****To insert data.txt content to collection
with open('data.txt') as json_file:
    data = json.load(json_file)
    for p in data:
        coll1.insert_one(p)

# Remove Dupes
# coll.ensureIndex( { "Quote":1 }, { unique:true, dropDups:true } )