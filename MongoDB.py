from pymongo import MongoClient
import pymongo
from AnyBDInterface import AnyBDInterface
from DB_Recorder import db_recorder


@db_recorder
class MongoDB(AnyBDInterface):
    def __init__(self, database, connection_string='mongodb://localhost:27017/?readPreference=primary&appname=MongoDB%20Compass&directConnection=true&ssl=false'):
        self.CONNECTION_STRING = connection_string
        self.client = MongoClient(self.CONNECTION_STRING)
        self.database = self.client[database]

    def try_connection(self) -> bool:
        pass

    def get_role_id_with_role_title(self, title) -> int:
        pass

    def check_exists_user_with_login(self, login) -> bool:
        pass

    def check_exists_city_with_title(self, title) -> bool:
        pass

    def get_customer_id_with_user_id(self, user_id) -> int:
        pass

    def sign_up_transaction(self, sign_up_tuple) -> bool:
        pass

    def order_completed_transaction(self, user_id) -> bool:
        pass

    def refusing_transaction(self, order_id) -> bool:
        pass

    def when_shall_i_be_free(self, user_id) -> bool:
        pass

    def customer_order_transaction(self, customer_order_tuple) -> bool:
        pass

    def get_user_id_with_login_and_password(self, login, password) -> int:
        pass

    def get_user_roles_with_users_id(self, users_id) -> tuple:
        pass

    def get_stage_id_with_stage_title(self, stage_title) -> int:
        pass

    def get_status_id_with_status_title(self, status_title) -> int:
        pass

    def alter_orders_status_id_with_order_id(self, orders_status, order_id) -> bool:
        pass

    def check_orders_executions_and_stage_id_with_order_id(self, order_id) -> tuple:
        pass

    def check_orders_status_id_with_order_id(self, order_id) -> int:
        pass

    def get_passive_orders_data_for_customer_with_customer_id(self, customer_id) -> tuple:
        pass

    def get_active_orders_data_for_customer_with_customer_id(self, customer_id) -> tuple:
        pass

    def get_services_costs_with_title(self, title) -> tuple:
        pass

    def get_city_titles(self) -> tuple:
        pass

    def check_exists_order_with_commissions_and_customer_id(self, commissions, customer_id) -> bool:
        pass

    def get_service_titles(self) -> tuple:
        pass

    def check_courier_id_not_null_with_order_id(self, order_id) -> bool:
        pass

    def get_free_couriers(self) -> tuple:
        pass

    def get_paid_orders(self) -> tuple:
        pass

    def get_services_titles_and_total_costs(self) -> tuple:
        pass

    def get_months_quantity_orders(self) -> tuple:
        pass

    def get_cities_quantity_orders(self) -> tuple:
        pass

    def get_fleet_titles(self) -> tuple:
        pass

    def get_kind_titles(self) -> tuple:
        pass

    def get_city_fields_with_title(self, title) -> tuple:
        pass

    def get_service_fields_with_title(self, title) -> tuple:
        pass

    def get_kind_fields_with_title(self, title) -> tuple:
        pass

    def get_fleet_fields_with_title(self, title) -> tuple:
        pass

    def alter_city_using_str_collection(self, data):
        pass

    def alter_service_using_str_collection(self, data):
        pass

    def alter_kind_using_str_collection(self, data):
        pass

    def alter_fleet_using_str_collection(self, data):
        pass

    def linking_transaction(self, operator_id, courier_id, order_id) -> bool:
        pass
