import pymongo
import json
from pandas import DataFrame
import datetime
from bson.objectid import ObjectId

CONNECTION_STRING = 'mongodb://localhost:27017/?readPreference=primary&appname=MongoDB%20Compass&directConnection=true&ssl=false'
DATABASE = 'coursework'


myclient = pymongo.MongoClient(CONNECTION_STRING)
mydb = myclient[DATABASE]
collections = mydb.list_collection_names()
mycol = mydb["handbooks"]


def _select_(database, select_, from_, where_=None) -> list:
    try:
        current_collection = database[from_]
        results = current_collection.find(select_)
        ans = [item for item in results]
        return ans
    except:
        return []


def _update_(database, update_, set_, where_) -> bool:
    try:
        current_collection = database[update_]
        current_collection.find_one_and_update(where_, {'$set': set_})
        return True
    except:
        return False


def _insert_(database, insert_into_, what_, values_=None) -> bool:
    try:
        current_collection = database[insert_into_]
        current_collection.insert_one(what_)
        return True
    except:
        return False


print(_insert_(mydb, "user", {"loki": "kali"}))
