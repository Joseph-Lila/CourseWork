import pymongo
from pymongo import MongoClient


class MongoDB:
    def __init__(self, host, port):
        client = MongoClient(host, port)
        print(client.list_database_names())
        db = client['coursework']
        print(db.list_collection_names())
        cw_collection = db['orders']
        print(cw_collection)

        new_order = {
            "customer": "me",
            "hero": 'god',
            'response person': 'nobody'
        }
        print(cw_collection.read_concern)

    @staticmethod
    def insert_document(collection, data):
        return collection.insert_one(data).inserted_id


if __name__ == "__main__":
    MongoDB("localhost", 27017)
