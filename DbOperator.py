from AnyBDInterface import AnyBDInterface
import MSSql, MongoDB, DB_Recorder


class DbOperator(AnyBDInterface):
    def __init__(self):
        self.representatives_collection = DB_Recorder.db_representatives

    def try_connection(self) -> bool:
        results = [item.try_connection() for item in self.representatives_collection]
        return self.__check_true_collection(results)

    @staticmethod
    def __check_equal(results) -> bool:
        if len(results) == 0:
            return False
        first = results[0]
        for i in range(len(results)):
            if first != results[i]:
                return False
        return True

    @staticmethod
    def __check_true_collection(results) -> bool:
        if len(results) == 0:
            return False
        for item in results:
            if item is False:
                return False
        return True

    @staticmethod
    def __get_outcomes_value(results, ans_type):
        if DbOperator().__check_equal(results):
            return results[-1]
        if ans_type == 'str':
            return ''
        if ans_type == 'bool':
            return False
        if ans_type == 'tuple':
            return tuple()
        if ans_type == 'int':
            return -1
        if ans_type == 'float':
            return -1
        if ans_type == 'list':
            return []
        if ans_type == 'set':
            return set()
        return None

    def check_exists_user_with_login(self, login) -> bool:
        results = [item.check_exists_user_with_login(login) for item in self.representatives_collection]
        return self.__get_outcomes_value(results, 'bool')

    def check_exists_city_with_title(self, title) -> bool:
        results = [item.check_exists_city_with_title(title) for item in self.representatives_collection]
        return self.__get_outcomes_value(results, bool)

    def sign_up_transaction(self, sign_up_tuple) -> bool:
        results = [item.sign_up_transaction(sign_up_tuple) for item in self.representatives_collection]
        return self.__check_true_collection(results)

    def is_user_plays_the_role(self, role_title, user_id) -> bool:
        results = [item.is_user_plays_the_role(role_title, user_id[i])
                   for i, item in enumerate(self.representatives_collection, start=0)]
        return self.__get_outcomes_value(results, 'bool')

    def get_user_id_with_login_and_password(self, login, password) -> tuple:
        return tuple([item.get_user_id_with_login_and_password(login, password)
                      for item in self.representatives_collection])

    def get_user_roles_with_users_id(self, users_id) -> tuple:
        results = [item.get_user_roles_with_users_id(users_id[i])
                   for i, item in enumerate(self.representatives_collection, start=0)]
        return self.__get_outcomes_value(results, 'tuple')

    def when_shall_i_be_free(self, user_id) -> bool:
        results = [item.when_shall_i_be_free(user_id[i])
                   for i, item in enumerate(self.representatives_collection, start=0)]
        return self.__check_true_collection(results)

    def refusing_transaction(self, order_id) -> bool:
        results = [item.refusing_transaction(order_id[i])
                   for i, item in enumerate(self.representatives_collection, start=0)]
        return self.__check_true_collection(results)

    def get_passive_orders_data_for_customer_with_customer_id(self, customer_id) -> tuple:
        return tuple([item.get_passive_orders_data_for_customer_with_customer_id(customer_id[i])
                      for i, item in enumerate(self.representatives_collection, start=0)])

    def get_active_orders_data_for_customer_with_customer_id(self, customer_id) -> tuple:
        return tuple([item.get_active_orders_data_for_customer_with_customer_id(customer_id[i])
                      for i, item in enumerate(self.representatives_collection, start=0)])

    def alter_orders_status_with_order_id(self, orders_status, order_id, status_description) -> bool:
        results = [item.alter_orders_status_with_order_id(orders_status, order_id[i], status_description)
                   for i, item in enumerate(self.representatives_collection, start=0)]
        return self.__check_true_collection(results)

    def get_services_costs_with_title(self, title) -> tuple:
        results = [item.get_services_costs_with_title(title) for item in self.representatives_collection]
        return self.__get_outcomes_value(results, 'tuple')

    def get_city_titles(self) -> tuple:
        results = [item.get_city_titles() for item in self.representatives_collection]
        results = [set(item) for item in results]
        return self.__get_outcomes_value(results, 'tuple')

    def get_fleet_titles(self) -> tuple:
        results = [item.get_fleet_titles() for item in self.representatives_collection]
        results = [set(item) for item in results]
        return self.__get_outcomes_value(results, 'tuple')

    def get_kind_titles(self) -> tuple:
        results = [item.get_kind_titles() for item in self.representatives_collection]
        results = [set(item) for item in results]
        return self.__get_outcomes_value(results, 'tuple')

    def get_services_titles_and_total_costs(self) -> tuple:
        results = [self.representatives_collection[0].get_services_titles_and_total_costs()]
        return self.__get_outcomes_value(results, 'tuple')

    def get_months_quantity_orders(self) -> tuple:
        results = [self.representatives_collection[0].get_months_quantity_orders()]
        return self.__get_outcomes_value(results, 'tuple')

    def get_cities_quantity_orders(self) -> tuple:
        results = [self.representatives_collection[0].get_cities_quantity_orders()]
        return self.__get_outcomes_value(results, 'tuple')

    def check_exists_order_with_commissions_and_customer_id(self, commissions, customer_id) -> bool:
        results = [item.check_exists_order_with_commissions_and_customer_id(commissions, customer_id)
                   for item in self.representatives_collection]
        return self.__check_true_collection(results)

    def customer_order_transaction(self, orders_service_tuples) -> bool:
        results = [item.customer_order_transaction(orders_service_tuples)
                   for item in self.representatives_collection]
        return self.__check_true_collection(results)

    def order_completed_transaction(self, user_id) -> bool:
        results = [item.order_completed_transaction(user_id[i])
                   for i, item in enumerate(self.representatives_collection, start=0)]
        return self.__check_true_collection(results)

    def get_service_titles(self) -> tuple:
        results = [item.get_service_titles() for item in self.representatives_collection]
        results = [set(item) for item in results]
        return self.__get_outcomes_value(results, 'tuple')

    def check_courier_id_not_null_with_order_id(self, order_id) -> bool:
        results = [item.check_courier_id_not_null_with_order_id(order_id) for item in self.representatives_collection]
        return self.__check_true_collection(results)

    def linking_transaction(self, operator_id, courier_id, order_id) -> bool:
        results = [item.linking_transaction(operator_id[i], courier_id[i], order_id[i])
                   for i, item in enumerate(self.representatives_collection, start=0)]
        return self.__check_true_collection(results)

    def get_paid_orders(self) -> tuple:
        return tuple([item.get_paid_orders() for item in self.representatives_collection])

    def get_free_couriers(self) -> tuple:
        return tuple([item.get_free_couriers() for item in self.representatives_collection])

    def get_city_fields_with_title(self, title) -> tuple:
        return tuple([item.get_city_fields_with_title(title) for item in self.representatives_collection])

    def alter_city_using_str_collection(self, data):
        for i, item in enumerate(self.representatives_collection, start=0):
            item.alter_city_using_str_collection(data[i])

    def get_service_fields_with_title(self, title) -> tuple:
        return tuple([item.get_service_fields_with_title(title) for item in self.representatives_collection])

    def get_kind_fields_with_title(self, title) -> tuple:
        return tuple([item.get_kind_fields_with_title(title) for item in self.representatives_collection])

    def get_fleet_fields_with_title(self, title) -> tuple:
        return tuple([item.get_fleet_fields_with_title(title) for item in self.representatives_collection])

    def alter_service_using_str_collection(self, data):
        for i, item in enumerate(self.representatives_collection, start=0):
            item.alter_service_using_str_collection(data[i])

    def alter_kind_using_str_collection(self, data):
        for i, item in enumerate(self.representatives_collection, start=0):
            item.alter_kind_using_str_collection(data[i])

    def alter_fleet_using_str_collection(self, data):
        for i, item in enumerate(self.representatives_collection, start=0):
            item.alter_fleet_using_str_collection(data[i])
