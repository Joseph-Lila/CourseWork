import pyodbc
import pandas as pd

tables = [
    ("stage", 2, "csv/stage.csv"),
    ("statuses", 2, "csv/status.csv"),
    ("transports_kind", 4, "csv/transports_kind.csv"),
    ("city", 1, "csv/city.csv"),
    ("roles", 2, "csv/role.csv"),
    ("users", 4, "csv/user.csv"),
    ("fleet", 6, "csv/fleet.csv"),
    ("services", 4, "csv/service.csv"),
    ("customer", 8, "csv/customer.csv"),
    ("customers_city", 2, "csv/customers_city.csv"),
    ("employee", 6, "csv/employee.csv"),
    ("users_role", 2, "csv/users_role.csv"),
    ("transport", 2, "csv/transport.csv"),
    ("my_order", 7, "csv/my_order.csv"),
    ("orders_transport", 2, "csv/orders_transport.csv"),
    ("orders_service", 9, "csv/orders_service.csv")
]


class Sql:
    def __init__(self, database, server='DESKTOP-7BD3QHU'):
        self.connector = pyodbc.connect('Driver={SQL Server Native Client 11.0};'
                                        'Server='+server+';'
                                        'Database='+database+';'
                                        'Trusted_Connection=yes;')

    def fill_the_table_from_csv(self, table, quantity_values, filename):
        df = pd.read_csv(filename, delimiter=";", header=None)
        insert_str = f"INSERT INTO {table} VALUES ("+'?,' * (quantity_values - 1)+'?'+")"
        cursor = self.connector.cursor()
        cursor.fast_executemany = True
        cursor.executemany(insert_str, df.values.tolist())
        print(f'{len(df)} rows inserted to the {table} table')
        cursor.commit()
        cursor.close()

    def gone_mad(self):
        self.connector.close()


def main():
    sql = Sql('Coursework_MSSQL')
    for table in tables:
        sql.fill_the_table_from_csv(*table)
    sql.gone_mad()


if __name__ == "__main__":
    main()
