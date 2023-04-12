import pymongo
from pymongo import MongoClient

client = MongoClient('mongodb://localhost:27017/')
db = client.ecom
collection = db.Users


def reguser(username, email, password):
    print(username)
    print(email)
    print(password)
    try:
        db.Users.insert({"username": username, "email": email, "password": password})
        result = True
        return result
    except Exception as e:
        print(e)
        result = False
        return result
