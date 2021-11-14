from AnyBDInterface import AnyBDInterface
import MSSql, DB_Recorder


class DbOperator(AnyBDInterface):
    def __init__(self):
        self.representatives_collection = DB_Recorder.db_representatives

    def try_connection(self) -> bool:
        results = []
        for item in self.representatives_collection:
            results.append(item.try_connection())
        return self.__check_true_collection(results)

    def confirm_changes(self):
        for item in self.representatives_collection:
            item.confirm_changes()

    def rollback_changes(self):
        for item in self.representatives_collection:
            item.rollback_changes()

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

    def __make_true_decision(self, results) -> bool:
        if self.__check_true_collection(results):
            self.confirm_changes()
            return True
        else:
            self.rollback_changes()
            return False

    def __make_a_decision(self, results) -> bool:
        if self.__check_equal(results):
            self.confirm_changes()
            return True
        else:
            self.rollback_changes()
            return False

    def __get_outcomes_value(self, results):
        if self.__check_equal(results):
            return results[0]
        return None

    def check_exists_user_with_login(self, login) -> bool:
        results = list()
        for item in self.representatives_collection:
            results.append(item.check_exists_user_with_login(login))
        return self.__get_outcomes_value(results)

    def check_exists_city_with_title(self, title) -> bool:
        results = list()
        for item in self.representatives_collection:
            results.append(item.check_exists_city_with_title(title))
        return self.__get_outcomes_value(results)

    def create_user(self, login, password, email, phone_number) -> bool:
        results = []
        for item in self.representatives_collection:
            results.append(item.create_user(login, password, email, phone_number))
        return self.__make_true_decision(results)

    def get_user_id_with_login(self, login):
        results = list()
        for item in self.representatives_collection:
            results.append(item.get_user_id_with_login(login))
        return self.__get_outcomes_value(results)

    def delete_user_with_login(self, login) -> bool:
        results = []
        for item in self.representatives_collection:
            results.append(item.delete_user_with_login(login))
        return self.__get_outcomes_value(results)

    def create_customer(self, data_collection) -> bool:
        results = list()
        for item in self.representatives_collection:
            results.append(item.create_customer(data_collection))
        return self.__make_true_decision(results)

    def get_customer_id_with_user_id(self, user_id):
        results = []
        for item in self.representatives_collection:
            results.append(item.get_customer_id_with_user_id(user_id))
        return self.__get_outcomes_value(results)

    def get_city_id_with_city_title(self, title):
        results = []
        for item in self.representatives_collection:
            results.append(item.get_city_id_with_city_title(title))
        return self.__get_outcomes_value(results)

    def insert_customers_city(self, customer_id, city_id) -> bool:
        results = []
        for item in self.representatives_collection:
            results.append(item.insert_customers_city(customer_id, city_id))
        return self.__make_true_decision(results)

    def get_role_id_with_role_title(self, title) -> int:
        results = []
        for item in self.representatives_collection:
            results.append(item.get_role_id_with_role_title(title))
        return self.__get_outcomes_value(results)

    def insert_users_role(self, user_id, role_id) -> bool:
        results = []
        for item in self.representatives_collection:
            results.append(item.insert_users_role(user_id, role_id))
        return self.__make_true_decision(results)

    def sign_up_transaction(self, sign_up_tuple) -> bool:
        results = []
        for item in self.representatives_collection:
            results.append(item.sign_up_transaction(sign_up_tuple))
        return self.__check_true_collection(results)

    def get_user_id_with_login_and_password(self, login, password) -> int:
        results = []
        for item in self.representatives_collection:
            results.append(item.get_user_id_with_login_and_password(login, password))
        return self.__get_outcomes_value(results)

    def get_user_roles_with_users_id(self, users_id) -> tuple:
        results = []
        for item in self.representatives_collection:
            results.append(item.get_user_roles_with_users_id(users_id))
        return self.__get_outcomes_value(results)

    def get_order_id_with_courier_id(self, courier_id) -> int:
        results = []
        for item in self.representatives_collection:
            results.append(item.get_order_id_with_courier_id(courier_id))
        return self.__get_outcomes_value(results)

    def get_stage_id_with_stage_title(self, stage_title) -> int:
        results = []
        for item in self.representatives_collection:
            results.append(item.get_stage_id_with_stage_title(stage_title))
        return self.__get_outcomes_value(results)

    def get_status_id_with_status_title(self, status_title) -> int:
        results = []
        for item in self.representatives_collection:
            results.append(item.get_status_id_with_status_title(status_title))
        return self.__get_outcomes_value(results)

    def add_orders_executions_and_stage_id_with_order_id(self, orders_executions, stage_id, order_id) -> bool:
        results = []
        for item in self.representatives_collection:
            results.append(item.add_orders_executions_and_stage_id_with_order_id(orders_executions,
                                                                                 stage_id,
                                                                                 order_id
                                                                                 )
                           )
        return self.__check_true_collection(results)

    def check_orders_executions_and_stage_id_with_order_id(self, order_id) -> tuple:
        results = []
        for item in self.representatives_collection:
            results.append(item.check_orders_executions_and_stage_id_with_order_id(order_id))
        if self.__check_equal(results):
            return results[-1]
        return tuple()

    def check_orders_status_id_with_order_id(self, order_id) -> int:
        results = []
        for item in self.representatives_collection:
            results.append(item.check_orders_status_id_with_order_id(order_id))
        if self.__check_equal(results):
            return results[-1]
        return -1

    def get_passive_orders_data_for_customer_with_customer_id(self, customer_id) -> tuple:
        results = []
        for item in self.representatives_collection:
            results.append(item.get_passive_orders_data_for_customer_with_customer_id(customer_id))
        if self.__check_equal(results):
            return results[-1]
        return tuple()

    def get_active_orders_data_for_customer_with_customer_id(self, customer_id) -> tuple:
        results = []
        for item in self.representatives_collection:
            results.append(item.get_active_orders_data_for_customer_with_customer_id(customer_id))
        if self.__check_equal(results):
            return results[-1]
        return tuple()

    def alter_orders_status_id_with_order_id(self, orders_status, order_id) -> bool:
        results = []
        for item in self.representatives_collection:
            results.append(item.alter_orders_status_id_with_order_id(orders_status, order_id))
        return self.__check_true_collection(results)

    def get_services_costs_with_title(self, title) -> tuple:
        results = []
        for item in self.representatives_collection:
            results.append(item.get_services_costs_with_title(title))
        if self.__check_equal(results):
            return results[-1]
        return tuple()

    def get_city_titles(self) -> tuple:
        results = []
        for item in self.representatives_collection:
            results.append(item.get_city_titles())
        return self.__get_outcomes_value(results)

    def check_exists_order_with_commissions_and_customer_id(self, commissions, customer_id) -> bool:
        results = []
        for item in self.representatives_collection:
            results.append(item.check_exists_order_with_commissions_and_customer_id(commissions, customer_id))
        return self.__check_true_collection(results)

    def customer_order_transaction(self, customer_order_tuple) -> bool:
        results = []
        for item in self.representatives_collection:
            results.append(item.customer_order_transaction(customer_order_tuple))
        return self.__check_true_collection(results)

    def get_service_titles(self) -> tuple:
        results = []
        for item in self.representatives_collection:
            results.append(item.get_service_titles())
        if self.__check_equal(results):
            return results[-1]
        return tuple()

    def check_courier_id_not_null_with_order_id(self, order_id) -> bool:
        results = []
        for item in self.representatives_collection:
            results.append(item.check_courier_id_not_null_with_order_id(order_id))
        return self.__check_true_collection(results)

    def add_courier_id_and_operator_id_into_order_with_order_id(self,
                                                                courier_id,
                                                                operator_id,
                                                                stage_id,
                                                                order_id
                                                                ) -> bool:
        results = []
        for item in self.representatives_collection:
            results.append(item.add_courier_id_and_operator_id_into_order_with_order_id(courier_id,
                                                                                        operator_id,
                                                                                        stage_id,
                                                                                        order_id
                                                                                        )
                           )
        return self.__check_true_collection(results)

    def get_paid_orders(self) -> tuple:
        results = []
        for item in self.representatives_collection:
            results.append(item.get_paid_orders())
        return self.__get_outcomes_value(results)

    def get_free_couriers(self) -> tuple:
        results = []
        for item in self.representatives_collection:
            results.append(item.get_free_couriers())
        return self.__get_outcomes_value(results)
