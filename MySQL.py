import mysql.connector
from mysql.connector import Error


class MySQL:
    def __init__(self, host, user, password):
        self.__host = host
        self.__user = user
        self.__password = password

    def connect_host(self):
        connection = None
        try:
            connection = mysql.connector.connect(
                host=self.__host,
                user=self.__user,
                passwd=self.__password
            )
        except Error as e:
            pass
        return connection

    def connect_database(self, database):
        connection = None
        try:
            connection = mysql.connector.connect(
                host=self.__host,
                user=self.__user,
                passwd=self.__password,
                database=database
            )
        except Error as e:
            pass
        return connection

    @staticmethod
    def create_database(connection, query):
        try:
            cursor = connection.cursor()
            cursor.execute(query)
            cursor.close()
            connection.close()
            return True
        except Error as e:
            return False

    @staticmethod
    def execute_query(connection, query):
        try:
            cursor = connection.cursor()
            cursor.execute(query)
            connection.commit()
            cursor.close()
            connection.close()
            return True
        except Error as e:
            return False

    @staticmethod
    def execute_query_data(connection, query, data):
        try:
            cursor = connection.cursor()
            cursor.execute(query, data)
            connection.commit()
            cursor.close()
            connection.close()
            return True
        except Error as e:
            return False

    @staticmethod
    def inserting_many_records(connection, insert, values):
        try:
            cursor = connection.cursor()
            cursor.executemany(insert, values)
            connection.commit()
            cursor.close()
            connection.close()
            return True
        except Error as e:
            return False

    @staticmethod
    def execute_read_query(connection, query):
        result = None
        try:
            cursor = connection.cursor()
            cursor.execute(query)
            result = cursor.fetchall()
            cursor.close()
            connection.close()
            return result
        except Error as e:
            return None

    @staticmethod
    def dalete_database(connection, query):
        try:
            cursor = connection.cursor()
            cursor.execute(query)
            cursor.close()
            connection.close()
            return True
        except Error as e:
            return False
