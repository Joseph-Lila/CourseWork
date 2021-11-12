import pyodbc
import pandas as pd


class MSSql:
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

    def confirm_changes(self):
        self.cursor.commit()
        self.cursor.close()

    def rollback_changes(self):
        self.cursor.rollback()
        self.cursor.close()

    def __insert_into(self, table, quantity_values, data_collection):
        try:
            connector = pyodbc.connect(self.__connect_str)
            self.cursor = connector.cursor()
            insert_str = f"INSERT INTO {table} VALUES (" + '?,' * (quantity_values - 1) + '?' + ")"
            self.cursor.fast_executemany = True
            self.cursor.executemany(insert_str, data_collection)
            print(f'{len(data_collection)} rows inserted to the {table} table')
        except:
            self.rollback_changes()

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

    def select_where(self, what_, from_, where_) -> list:
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


tables = [
    ("stage", 2, "csv/stage.csv"),
    ("statuses", 2, "csv/status.csv"),
    ("transports_kind", 4, "csv/transports_kind.csv"),
    ("city", 1, "csv/city.csv"),
    ("roles", 2, "csv/role.csv"),
    ("users", 4, "csv/user.csv"),
    ("fleet", 5, "csv/fleet.csv"),
    ("services", 4, "csv/service.csv"),
    ("customer", 8, "csv/customer.csv"),
    ("customers_city", 2, "csv/customers_city.csv"),
    ("employee", 6, "csv/employee.csv"),
    ("users_role", 2, "csv/users_role.csv"),
    ("fleets_city", 2, "csv/fleets_city.csv"),
    ("transport", 2, "csv/transport.csv"),
    ("my_order", 7, "csv/my_order.csv"),
    ("orders_transport", 2, "csv/orders_transport.csv"),
    ("orders_service", 7, "csv/orders_service.csv"),
    ("order_services_begin_city", 2, "csv/order_services_begin_city.csv"),
    ("order_services_end_city", 2, "csv/order_services_end_city.csv"),
]

db = MSSql()
print(db.select_where(what_="*", from_="city", where_="city_id = 5"))
