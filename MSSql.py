from pymssql import *
from AnyBDInterface import AnyBDInterface
from DB_Recorder import db_recorder
import pyodbc
import pandas as pd


@db_recorder
class MSSql(AnyBDInterface):
    def __init__(
            self,
            driver="SQL Server Native Client 11.0",
            server='DESKTOP-7BD3QHU',
            database="Coursework_MSSQL",
            trusted_connection="yes"
    ):
        self.cursor = None
        self.__connect_str = """
        Driver={};
        Server={};
        Database={};
        Trusted_Connection={};
        """.format(
            driver,
            server,
            database,
            trusted_connection
        )

    def try_connection(self) -> bool:
        try:
            connector = pyodbc.connect(self.__connect_str)
            connector.close()
            return True
        except:
            return False

    def confirm_changes(self):
        self.cursor.commit()
        self.cursor.close()

    def rollback_changes(self):
        self.cursor.rollback()
        self.cursor.close()

    def __insert_into(self, table, quantity_values, data_collection) -> bool:
        try:
            connector = pyodbc.connect(self.__connect_str)
            self.cursor = connector.cursor()
            insert_str = f"INSERT INTO {table} VALUES (" + '?,' * (quantity_values - 1) + '?' + ")"
            self.cursor.fast_executemany = True
            self.cursor.executemany(insert_str, data_collection)
            return True
        except:
            return False

    def __select(self, what_, from_) -> list:
        try:
            connector = pyodbc.connect(self.__connect_str)
            self.cursor = connector.cursor()
            select_str = f"SELECT {what_} FROM {from_}"
            self.cursor.execute(select_str)
            ans = list()
            for item in self.cursor:
                ans.append(item)
            self.cursor.close()
            return ans
        except:
            return list()

    def __select_where(self, what_, from_, where_) -> list:
        try:
            connector = pyodbc.connect(self.__connect_str)
            self.cursor = connector.cursor()
            select_str = f"SELECT {what_} FROM {from_} WHERE {where_}"
            self.cursor.execute(select_str)
            ans = list()
            for item in self.cursor:
                ans.append(item)
            self.cursor.close()
            return ans
        except:
            return list()

    def __delete_where(self, what_, from_, value):
        connector = pyodbc.connect(self.__connect_str)
        self.cursor = connector.cursor()
        select_str = f"DELETE FROM {from_} WHERE {what_} = {value}"
        self.cursor.execute(select_str)
        self.cursor.close()

    def create_customer(self, data_collection):
        return self.__insert_into("customer", 8, [data_collection])

    def create_user(self, login, password, email, phone_number) -> bool:
        return self.__insert_into("users", 4, [(login, password, email, phone_number)])

    def get_user_id_with_login(self, login):
        results = self.__select_where("users_id", "users", f"login = '{login}'")
        if len(results) == 0:
            return -1
        return results[0][0]

    def delete_user_with_login(self, login) -> bool:
        try:
            self.__delete_where("users", "login", f"'{login}'")
            return True
        except:
            return False

    def insert_users_role(self, user_id, role_id) -> bool:
        return self.__insert_into("users_role", 2, [(user_id, role_id)])

    def get_role_id_with_role_title(self, title):
        results = self.__select_where("role_id", "roles", f"title = '{title}'")
        if len(results) == 0:
            return -1
        return results[0][0]

    def check_exists_city_with_title(self, title) -> bool:
        results = self.__select_where("city_id", "city", f"title = '{title}'")
        if len(results) == 0:
            return False
        return True

    def check_exists_user_with_login(self, login) -> bool:
        results = self.__select_where("users_id", "users", f"login = '{login}'")
        if len(results) == 0:
            return False
        return True

    def get_customer_id_with_user_id(self, user_id):
        results = self.__select_where("customer_id", "customer", f"users_id = {user_id}")
        if len(results) == 0:
            return -1
        return results[0][0]

    def get_city_id_with_city_title(self, title):
        results = self.__select_where("city_id", "city", f"title = '{title}'")
        if len(results) == 0:
            return -1
        return results[0][0]

    def insert_customers_city(self, customer_id, city_id) -> bool:
        return self.__insert_into("customers_city", 2, [(customer_id, city_id)])


if __name__ == "__main__":
    pass
