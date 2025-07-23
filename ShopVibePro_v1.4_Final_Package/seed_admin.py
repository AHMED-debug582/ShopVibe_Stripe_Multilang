from pymongo import MongoClient
import hashlib

client = MongoClient("mongodb://localhost:27017/")
db = client["shopvibe"]
admins = db["admins"]

username = "admin"
password = "123456"

hashed_password = hashlib.sha256(password.encode()).hexdigest()

admins.insert_one({
    "username": username,
    "password": hashed_password
})

print("✅ Admin created.")
