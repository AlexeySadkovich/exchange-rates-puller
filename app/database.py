import os
from typing import Dict, List

from pymongo import MongoClient

MONGO_HOST = os.getenv("MONGO_HOST")
MONGO_PORT = os.getenv("MONGO_PORT")
MONGO_DB = os.getenv("MONGO_INITDB_DATABASE")

MONGO_USER = os.getenv("MONGO_INITDB_ROOT_USERNAME")
MONGO_PASS = os.getenv("MONGO_INITDB_ROOT_PASSWORD")

client = MongoClient(MONGO_HOST, int(MONGO_PORT), username=MONGO_USER, password=MONGO_PASS)
db = client[MONGO_DB]


def save(entry: Dict) -> int:
    """Save exchange information to database"""
    collection = db['rates']
    entry_id = collection.insert_one(entry).inserted_id

    return entry_id


def get_all() -> List:
    """Return all saved currency rates"""
    entries = []
    collection = db['rates']

    for entry in collection.find():
        entries.append(entry)

    return entries
