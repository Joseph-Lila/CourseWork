from datetime import *
from dateutil import parser
from User import User
from pymongo import MongoClient
from AnyBDInterface import AnyBDInterface
from DBContract import DBContract
from DB_Recorder import db_recorder


@db_recorder
class MongoDB(AnyBDInterface, DBContract):
    def __init__(self, database='coursework', connection_string='mongodb://localhost:27017/?readPreference=primary&appname=MongoDB%20Compass&directConnection=true&ssl=false'):
        self.CONNECTION_STRING = connection_string
        self.client = MongoClient(self.CONNECTION_STRING)
        self.database = self.client[database]

    def _select_(self, select_, from_, where_=None) -> list:
        try:
            current_collection = self.database[from_]
            results = current_collection.find(select_)
            ans = [item for item in results]
            return ans
        except:
            return []

    def _update_(self, update_, set_, where_) -> bool:
        try:
            current_collection = self.database[update_]
            current_collection.find_one_and_update(where_, {'$set': set_})
            return True
        except:
            return False

    def _delete_(self, from_, where_) -> bool:
        try:
            current_collection = self.database[from_]
            current_collection.delete_one(where_)
            return True
        except:
            return False

    def _insert_(self, insert_into_, what_, values_=None) -> bool:
        try:
            current_collection = self.database[insert_into_]
            current_collection.insert_one(what_)
            return True
        except:
            return False

    def _execute_(self, what_) -> bool:
        return True

    def try_connection(self) -> bool:
        try:
            self.database.list_collection_names()
            return True
        except:
            return False

    def is_user_plays_the_role(self, role_title, user_id) -> bool:
        results = self._select_({"_id": user_id, "roles.role_title": role_title}, "user")
        if len(results) == 0:
            return False
        return True

    def check_exists_user_with_login(self, login) -> bool:
        results = self._select_({"login": login}, "user")
        if len(results) == 0:
            return False
        return True

    def check_exists_city_with_title(self, title) -> bool:
        results = self._select_({"city_title": title}, "handbooks")
        if len(results) == 0:
            return False
        return True

    def sign_up_transaction(self, sign_up_tuple) -> bool:
        return self._insert_("user",
                             {
                                 "status_title": None,
                                 "status_description": None,
                                 "country": sign_up_tuple.country,
                                 "street": sign_up_tuple.street,
                                 "home_number": sign_up_tuple.home_number,
                                 "flat_number": sign_up_tuple.flat_number,
                                 "last_name": sign_up_tuple.lastname,
                                 "name": sign_up_tuple.name,
                                 "middle_name": sign_up_tuple.middle_name,
                                 "login": sign_up_tuple.login,
                                 "password": sign_up_tuple.password,
                                 "email": sign_up_tuple.email,
                                 "phone_number": sign_up_tuple.phone_number,
                                 "salary": None,
                                 "passport_data": None,
                                 "requirements": None,
                                 "duties": None,
                                 "roles": [
                                     {
                                         "role_title": "Клиент",
                                         "role_description": "Заказывает платные услуги."
                                     }
                                 ]
                             }
                             )

    def order_completed_transaction(self, user_id) -> bool:
        ans1 = self._update_("my_order",
                             {"executions": parser.parse(datetime.now().strftime("%Y-%m-%d %H:%M:%S")),
                              "stage_title": "Выполнен",
                              "stage_description": "Заказ в процессе выполнения.",
                              },
                             {
                                 "courier_id": user_id,
                                 "stage_title": {"$not": "Выполнен"}
                             }
                             )
        ans2 = self._update_("user",
                             {
                                 "status_title": "Свободен",
                                 "status_description": "Сотрудник доступен и ему можно поручить задание."
                             },
                             {
                                 "_id": user_id
                             }
                             )
        return ans1 and ans2

    def refusing_transaction(self, order_id) -> bool:
        return self._update_(
            "my_order",
            {
                "stage_title": "Отменен",
                "stage_description": "Заказ не был оплачен и был отменен клиентом.",
                "executions": parser.parse(datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
            },
            {
                "_id": order_id
            }
        )

    def when_shall_i_be_free(self, user_id) -> bool:
        results = self._select_({"_id": user_id, "status_title": "Свободен"}, "user")
        if len(results) == 0:
            return False
        return True

    def customer_order_transaction(self, orders_service_tuples) -> bool:
        date_time = parser.parse(datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
        ans = self._insert_(
            "my_order",
            {
                "commissions": date_time,
                "executions": None,
                "stage_title": "На рассмотрении",
                "stage_description": "Заказ оплачен и должен быть поручен свободному курьеру.",
                "customer_id": User.user_id,
                "operator_id": None,
                "courier_id": None,
                "orders_services": [],
                "status_title": "Не оплачен",
                "status_description": "Заказ не оплачен и может быть отменен."
            }
        )
        for item in orders_service_tuples:
            self.orders_service_adding_transaction(item, date_time)
        return ans

    def get_current_orders_services(self, date_time) -> list:
        results = self._select_(
            {
                "commissions": date_time
            },
            "handbooks"
        )
        ans = [item["orders_services"] for item in results]
        return ans

    def orders_service_adding_transaction(self, orders_service_tuple, date_time) -> bool:
        current_orders_services = self.get_current_orders_services(date_time)
        current_service = self.get_service_fields_with_title(orders_service_tuple.title)
        current_begin_city_id = self.get_city_fields_with_title(orders_service_tuple.begin_city.text)[0]
        current_end_city_id = self.get_city_fields_with_title(orders_service_tuple.end_city.text)[0]
        current_orders_services.append(
            {
                "service_id": current_service[0],
                "service_title": current_service[1],
                "quantity_weight": float(orders_service_tuple.weight.text),
                "quantity_radius": float(orders_service_tuple.radius.text),
                "total_cost": float(orders_service_tuple.total_cost.text),
                "destination": orders_service_tuple.destination.text,
                "departure": orders_service_tuple.departure.text,
                "begin_city_id": current_begin_city_id,
                "end_city_id": current_end_city_id
            }
        )
        return self._update_(
            "my_order",
            {
                "orders_services": current_orders_services
            },
            {
                "commissions": date_time
            }
        )

    def get_user_id_with_login_and_password(self, login, password) -> int:
        results = self._select_(
            {
                "login": login,
                "password": password
            },
            "user"
        )
        if len(results) == 0:
            return -1
        return results[0]['_id']

    def get_user_roles_with_users_id(self, users_id) -> tuple:
        results = self._select_(
            {
                "_id": users_id
            },
            "user"
        )
        ans = results[0]["roles"]
        if len(ans) == 0:
            return ()
        return tuple((item["role_title"] for item in ans))

    def get_passive_orders_data_for_customer_with_customer_id(self, customer_id) -> tuple:
        results = self._select_(
            {
                "stage_title": {"$not": ["На рассмотрении", "Выполняется"]},
                "customer_id": customer_id
            },
            "my_order"
        )
        ans = tuple([item['_id'], item['commissions'], item['executions'], item['status_title'], item['stage_title']]
                    for item in results
                    )
        if len(ans) == 0:
            return ()
        return ans

    def get_active_orders_data_for_customer_with_customer_id(self, customer_id) -> tuple:
        results = self._select_(
            {
                "stage_title": {"$or": ["На рассмотрении", "Выполняется"]},
                "customer_id": customer_id
            },
            "my_order"
        )
        ans = tuple(
            (
                [item['_id'], item['commissions'], item['executions'], item['status_title'], item['stage_title']]
                for item in results
            )
        )
        if len(ans) == 0:
            return ()
        return ans

    def get_services_costs_with_title(self, title) -> tuple:
        results = self._select_(
            {"service_title": title},
            "handbooks"
        )
        if len(results) == 0:
            return tuple()
        return results[0]["cost_weight"], results[0]["cost_radius"]

    def get_city_titles(self) -> tuple:
        results = self._select_(
            {},
            "handbooks"
        )
        return tuple((item["city_title"] for item in results if "city_title" in item.keys()))

    def check_exists_order_with_commissions_and_customer_id(self, commissions, customer_id) -> bool:
        results = self._select_(
            {
                "commissions": commissions,
                "customer_id": customer_id
            },
            "my_order"
        )
        if len(results) == 0:
            return False
        return True

    def get_service_titles(self) -> tuple:
        results = self._select_(
            {},
            "handbooks"
        )
        return tuple((item["service_title"] for item in results if "service_title" in item.keys()))

    def check_courier_id_not_null_with_order_id(self, order_id) -> bool:
        results = self._select_(
            {
                "_id": order_id
            },
            "my_order"
        )
        if len(results) == 0:
            return False
        if results[0]["courier_id"] is None:
            return False
        return True

    def get_free_couriers(self) -> tuple:
        results = self._select_(
            {
                "roles.title": "Курьер",
                "status_title": "Свободен"
            },
            "users"
        )
        if len(results) == 0:
            return tuple()
        return tuple((item["_id"] for item in results))

    def get_paid_orders(self) -> tuple:
        results = self._select_(
            {
                "stage_title": "На рассмотрении",
                "status_title": "Оплачен"
            },
            "my_order"
        )
        if len(results) == 0:
            return tuple()
        return tuple((item["_id"] for item in results))

    def get_services_titles_and_total_costs(self) -> tuple:
        results = self.database["handbooks"].aggregate(
            [
                {
                    "$group": {
                        "service_title": "$service_title",
                        "total_cost": {
                            "$sum": "$total_cost"
                        }
                    }
                }
            ]
        )
        if len(results) == 0:
            return tuple()
        return tuple(
            [item["service_title"], item['total_cost']] for item in results
        )

    def get_months_quantity_orders(self) -> tuple:
        results = self.database["my_order"].aggregate(
            [
                {
                    "$group": {
                        "months": {
                            "$month": "$commissions"
                        },
                        "quantity": {
                            "$count": "$_id"
                        }
                    }
                }
            ]
        )
        if len(results) == 0:
            return tuple()
        return tuple(
            [datetime.date(1900, item["months"], 1).strftime('%B'), item['quantity']]
            for item in results
        )

    def get_cities_quantity_orders(self) -> tuple:
        results = self.database["my_order"].aggregate(
            [
                {
                    "$group": {
                        "service_title": "$orders_services.begin_city_id",
                        "total_cost": {
                            "$count": "$orders_services.service_id"
                        }
                    }
                }
            ]
        )
        if len(results) == 0:
            return tuple()
        return tuple(
            [item["service_title"], item['total_cost']] for item in results
        )

    def get_fleet_titles(self) -> tuple:
        pass

    def get_kind_titles(self) -> tuple:
        pass

    def get_city_fields_with_title(self, title) -> tuple:
        result = self._select_(
            {},
            "handbooks"
        )
        ans = [item for item in result if "city_title" in item.keys() and item["city_title"] == title]
        if len(ans) == 0:
            return tuple()
        ans = tuple([ans[0]["_id"], ans[0]["city_title"]])
        return ans

    def get_service_fields_with_title(self, title) -> tuple:
        result = self._select_(
            {},
            "handbooks"
        )
        ans = [item for item in result if "service_title" in item.keys() and item["service_title"] == title]
        if len(ans) == 0:
            return tuple()
        ans = tuple([
            ans[0]["_id"],
            ans[0]["service_title"],
            ans[0]["service_description"],
            ans[0]["cost_weight"],
            ans[0]["cost_radius"]
        ]
        )
        return ans

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

    def alter_orders_status_with_order_id(self, status_title, order_id, status_description=None) -> bool:
        return self._update_("my_order",
                             {"status_title": status_title,
                              "status_description": status_description,
                              },
                             {
                                 "_id": order_id
                             }
                             )
