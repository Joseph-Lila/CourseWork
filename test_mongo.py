from pymongo import MongoClient
import pymongo
from dateutil import parser
from pandas import DataFrame


class MongoDB():
    def __init__(self, database='coursework', connection_string='mongodb://localhost:27017/?readPreference=primary&appname=MongoDB%20Compass&directConnection=true&ssl=false'):
        self.CONNECTION_STRING = connection_string
        self.client = MongoClient(self.CONNECTION_STRING)
        self.database = self.client[database]

    def get_database(self):
        return self.database


if __name__ == "__main__":
    dbname = MongoDB().get_database()
    collection_name = dbname["my_order"]
    # collection_name.drop()
    item_details = collection_name.find()
    print(item_details[0])
    items_df = DataFrame(item_details)
    print(items_df)
    #category_index = collection_name.create_index('poki')
