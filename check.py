from pymongo import MongoClient

# Establish a connection to MongoDB
client = MongoClient("mongodb://localhost:27017/")  # Replace with your MongoDB URI
db = client["irctc"]  # Replace with your database name
collection = db["users"]  # Replace with your collection name

# Document to insert
 new_document = {
    "username": "user1",
    "password": "1234",
    # Example field for department admin
    "is_admin":False,
    "c_a":False,
    "s_a":False,
    "o_a":False
} 

# Insert the document into the collection
result = collection.insert_one(new_document)

# Print the ID of the inserted document
print(f"Document inserted with ID: {result.inserted_id}")

