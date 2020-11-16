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


def get_rates_data(params: Dict) -> List:
    """Return all saved currency rates"""
    entries = []
    collection = db['rates']

    filter_by = params["filter"]
    sort_by = params["sort_by"]
    order = int(params["order"])

    if len(sort_by) > 0:
        if len(filter_by) > 0:
            sort_by = sort_by.replace(" ", "-").lower()

            for entry in collection.find({"currency": filter_by}).sort(sort_by, order):
                entries.append(entry)
        else:
            for entry in collection.find().sort(sort_by, order):
                entries.append(entry)
    else:
        if len(filter_by) > 0:
            for entry in collection.find({"currency": filter_by}):
                entries.append(entry)
        else:
            for entry in collection.find():
                entries.append(entry)

    return entries
