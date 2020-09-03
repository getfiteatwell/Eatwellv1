import pymongo

client = pymongo.MongoClient("mongodb://localhost:27017")
db = client["db"]

#database objects
profiledb = db["profiles"]
postsdb = db["posts"]
tasksdb = db["tasks"]
classdb = db["classes"]
updatedb = db["update"]