import os
from datetime import date, datetime
from typing import Dict, List, Optional

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


def get_rates_data(params: Dict) -> (Optional[List], Optional[str]):
    """Return saved currency rates with applied filters and sorting"""
    entries = []
    collection = db['rates']

    filter_by = params["filter"]
    sort_by = params["sort_by"]
    order = int(params["order"])
    date_from = params["date-from"]
    date_to = params["date-to"]

    if len(date_to) == 0 or datetime.strptime(date_to, "%Y-%m-%d").date() > datetime.now().date():
        date_to = date.today().strftime("%Y-%m-%d")

    if len(date_from) > 0 and datetime.strptime(date_from, "%Y-%m-%d").date() > datetime.now().date():
        return None, "Invalid date"

    if len(date_from) == 0:
        date_from = date(1970, 1, 1).strftime("%Y-%m-%d")

    filter_params = {
        "date-from": {"$gte": date_from},
        "date-to": {"$lte": date_to}
    }

    if len(filter_by) > 0:
        filter_params["currency"] = filter_by

    if len(sort_by) > 0:
        sort_by = sort_by.replace(" ", "-").lower()

        for entry in collection.find(filter_params).sort(sort_by, order):
            entries.append(entry)
    else:
        for entry in collection.find(filter_params):
            entries.append(entry)

    if len(entries) == 0:
        return None, "Entries not found"

    return entries, None
