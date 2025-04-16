from pymongo import MongoClient

client = MongoClient("mongodb://localhost:27017/")
db = client["irctc"]
get_user_collection = db["users"]
get_complaints_collection = db["complaints"]
