import pymongo
import json
import bson
from pandas import DataFrame
from datetime import *
from bson.objectid import ObjectId
from dateutil import parser

CONNECTION_STRING = 'mongodb://localhost:27017/?readPreference=primary&appname=MongoDB%20Compass&directConnection=true&ssl=false'
DATABASE = 'coursework'


myclient = pymongo.MongoClient(CONNECTION_STRING)
mydb = myclient[DATABASE]
collections = mydb.list_collection_names()
mycol = mydb["my_order"]


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


def get_services_titles_and_total_costs(database):
    pipe2 = [
        {
            "$unwind": "$orders_services.service_title"
        },
        {
            "$group": {
                "_id": "$orders_services.service_title",
                "total_cost": {"$sum": "$orders_services.total_cost"},
            }
        }
    ]
    results = database["my_order"].aggregate(pipeline=pipe2)
    for x in results:
        print(x)


get_services_titles_and_total_costs(mydb)