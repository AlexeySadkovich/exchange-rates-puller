import os

from pymongo import MongoClient


MONGO_HOST = os.getenv("MONGO_HOST")
MONGO_PORT = os.getenv("MONGO_PORT")

client = MongoClient(MONGO_HOST, MONGO_PORT)
db = client.currency


def save_rates():
    pass
