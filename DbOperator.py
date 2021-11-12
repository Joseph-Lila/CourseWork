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
        print(self.__get_outcomes_value(results))
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

    def get_role_id_with_role_title(self, title):
        results = []
        for item in self.representatives_collection:
            results.append(item.get_role_id_with_role_title(title))
        return self.__get_outcomes_value(results)

    def insert_users_role(self, user_id, role_id) -> bool:
        results = []
        for item in self.representatives_collection:
            results.append(item.insert_users_role(user_id, role_id))
        return self.__make_true_decision(results)
