import os
from typing import Dict, List

from pymongo import MongoClient


MONGO_HOST = os.getenv("MONGO_HOST")
MONGO_PORT = os.getenv("MONGO_PORT")
MONGO_DB = os.getenv("MONGO_INITDB_DATABASE")

client = MongoClient(MONGO_HOST, MONGO_PORT)
db = client[MONGO_DB]
collection = db['rates']


def save(name: str, data: Dict) -> Dict:
    """Save exchange information to database"""
    entry = {name: data}
    collection.insert_one(entry)
    return entry


def get_all() -> List:
    """Return all saved currency rates"""
    entries = []
    for entry in collection.find():
        entries.append(entry)

    return entries
