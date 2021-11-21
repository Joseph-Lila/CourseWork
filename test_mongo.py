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
print(collections)
mycol = mydb["handbooks"]

# mycol.drop()
# with open('Databases/MongoDB/configs/my_order.json') as f:
#     file_data = json.load(f)
#
# mycol.insert_one(file_data)

for x in mycol.find({}):
    print(x)
