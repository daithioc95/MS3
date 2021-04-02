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
documents = coll1.find()

# coll2.update_one({"Author":"C.S. Lewis"},{"$set": {"Books": k[1]}})

# write all books & authors to author db -- Tested
# store_authors = []
# coll2.delete_many({})
# for doc in documents:
#     if doc["Author"] not in store_authors:
#         store_authors.append(doc["Author"])
#         coll2.insert_one({"Author":doc["Author"]})
#         coll2.update_one({"Author":doc["Author"]}, { "$addToSet": { "Books":doc["Book"]}})
#         coll2.update_one({"Author":doc["Author"]}, { "$addToSet": { "Categories":doc["Category"]}})
#     else:
#         coll2.update_one({"Author":doc["Author"]}, { "$addToSet": { "Books":doc["Book"]}})
#         coll2.update_one({"Author":doc["Author"]}, { "$addToSet": { "Categories":doc["Category"]}})

# write all unique authors to author db (not necessarily needed) -- Tested
# store_authors = []
# coll2.delete_many({})
# for doc in documents:
#     if doc["Author"] not in store_authors:
#         coll2.insert_one({"Author":doc["Author"], "Books": doc["Book"]})
# print(store_authors)


# ****To split and update the Author and Books fields --tested
# for doc in documents_authors:
#     k = doc["Author"].split(",")
#     try:
#         coll1.update_one({"Author":doc["Author"]},{"$set": {"Book": k[1]}})
#         coll1.update_one({"Author":doc["Author"]},{"$set": {"Author": k[0]}})
#     except:
#         pass

# ***Adding category to entire list --tested
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


# Upload quotes from data.txt to quotes collection


# *** Delete all documents --tested
# coll1.delete_many({})

# *****To insert data.txt content to collection --tested
# with open('data.txt') as json_file:
#     data = json.load(json_file)
#     for p in data:
#         coll1.insert_one(p)

# Remove Dupes
# coll.ensureIndex( { "Quote":1 }, { unique:true, dropDups:true } )