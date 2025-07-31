from pymongo import MongoClient
import os

MONGODB_URL = "mongodb://mongo:27017/"
MONGODB_DB_NAME ="patient_management"

client = MongoClient(MONGODB_URL)
db = client[MONGODB_DB_NAME]

def get_database():
    return db
