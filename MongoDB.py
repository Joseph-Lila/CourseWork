from pymongo import MongoClient
from AnyBDInterface import AnyBDInterface
from DB_Recorder import db_recorder


@db_recorder
class MongoDB(AnyBDInterface):
    '''
    def __init__(self, host, port, database):
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
    '''
    @staticmethod
    def insert_document(collection, data):
        return collection.insert_one(data).inserted_id

    def create_customer(self, data_collection):
        pass

    def get_services_collection(self) -> set:
        pass

    def create_order(self, data_collection):
        pass

    def get_active_orders(self) -> set:
        pass

    def get_passive_orders(self) -> set:
        pass

    def get_free_courier_ids(self) -> set:
        pass

    def get_free_order_ids(self) -> set:
        pass

    def check_exists_user_with_login(self) -> bool:
        return False

    def check_exists_city_with_title(self) -> bool:
        return True

    def create_user(self, data_collection):
        pass


if __name__ == "__main__":
    pass