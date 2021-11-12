from MySQL import *
import csv


class MyDatabase:
    def __init__(self, host, user, password):
        self.__sql_pointer = MySQL(host, user, password)
        self.__connection = None
        self.__database = None
        self.tables_names = [
            'stage',
            'status',
            'transports_kind',
            'city',
            'role',
            'user',
            'fleet',
            'service',
            'customer',
            'customers_city',
            'employee',
            'users_role',
            'fleets_city',
            'transport',
            'my_order',
            'orders_transport',
            'orders_service',
            'order_services_begin_city',
            'order_services_end_city'
        ]
        self.__insert_constructions = [
            """INSERT INTO stage (  
                        title, 
                        description 
                    ) 
                    VALUES ( %s, %s )
                    """, #stage
            """INSERT INTO status (  
                        title, 
                        description 
                    ) 
                    VALUES ( %s, %s )
                    """, #status
            """INSERT INTO transports_kind (  
                        description, 
                        title, 
                        lifting_capacity, 
                        volume
                    ) 
                    VALUES ( %s, %s, %s, %s )
                    """, #transports_kind
            """INSERT INTO city (   
                        title 
                    ) 
                    VALUES ( %s )
                    """, #city
            """INSERT INTO role ( 
                        description, 
                        title
                    ) 
                    VALUES ( %s, %s )
                    """, #role
            """INSERT INTO user ( 
                        login,
                        password,
                        email,
                        phone_number
                    ) 
                    VALUES ( %s, %s, %s, %s )
                    """, #user
            """INSERT INTO fleet (  
                        title, 
                        description, 
                        address,
                        square,
                        stars_quantity
                    ) 
                    VALUES ( %s, %s, %s, %s, %s )
                    """, #fleet
            """INSERT INTO service (  
                        title, 
                        description, 
                        cost_weight, 
                        cost_radius
                    ) 
                    VALUES ( %s, %s, %s, %s )
                    """, #service
            """INSERT INTO customer ( 
                    user_id,
                    country,
                    street,
                    home_number,
                    flat_number,
                    lastname,
                    name,
                    middle_name
                ) 
                VALUES ( %s, %s, %s, %s, %s, %s, %s, %s )
                """, #customer
            """INSERT INTO customers_city ( 
                        customer_id,
                        city_id
                    ) 
                    VALUES ( %s, %s )
                    """, #customers_city
            """INSERT INTO employee ( 
                        user_id,
                        passport_data,
                        salary,
                        requirements,
                        duties,
                        status
                    ) 
                    VALUES ( %s, %s, %s, %s, %s, %s )
                    """, #employee
            """INSERT INTO users_role ( 
                        user_id,
                        role_id
                    ) 
                    VALUES ( %s, %s )
                    """, #users_role
            """INSERT INTO fleets_city ( 
                        fleet_id,
                        city_id
                    ) 
                    VALUES ( %s, %s )
                    """, #fleets_city
            """INSERT INTO transport ( 
                        kind_id,
                        fleet_id
                    ) 
                    VALUES ( %s, %s )
                    """, #transport
            """INSERT INTO my_order ( 
                        commissions,
                        executions,
                        customer_id,
                        operator_id,
                        courier_id,
                        stage_id,
                        status_id,
                    ) 
                    VALUES ( %s, %s, %s, %s, %s, %s, %s )
                    """, #order
            """INSERT INTO orders_transport ( 
                    transport_id,
                    my_order_id
                ) 
                VALUES ( %s, %s )
                """, #orders_transport
            """INSERT INTO orders_service ( 
                    service_id,
                    my_order_id,
                    quantity_weight,
                    quantity_radius,
                    destinations_address,
                    departures_address,
                    total_cost
                ) 
                VALUES ( %s, %s, %s, %s, %s, %s, %s )
                """, #orders_service
            """INSERT INTO order_services_begin_city ( 
                    city_id,
                    orders_service_id
                ) 
                VALUES ( %s, %s )
                """, #order_services_begin_city
            """INSERT INTO order_services_end_city ( 
                        city_id,
                        orders_service_id
                    ) 
                    VALUES ( %s, %s )
                    """  #order_services_end_city
        ]
        self.__alter_constructions = [
            """
                ALTER TABLE customer ADD CONSTRAINT fk_customer__user
                FOREIGN KEY (user_id) REFERENCES user(user_id) 
                ON UPDATE CASCADE ON DELETE CASCADE;
                """,
            """
                ALTER TABLE customers_city ADD CONSTRAINT fk_customers_city__city
                FOREIGN KEY (city_id) REFERENCES city(city_id) 
                ON UPDATE CASCADE ON DELETE CASCADE;
                """,
            """
                ALTER TABLE customers_city ADD CONSTRAINT fk_customers_city__customer
                FOREIGN KEY (customer_id) REFERENCES customer(customer_id) 
                ON UPDATE CASCADE ON DELETE CASCADE;
                """,
            """
                ALTER TABLE employee ADD CONSTRAINT fk_employee__user
                FOREIGN KEY (user_id) REFERENCES user(user_id) 
                ON UPDATE CASCADE ON DELETE CASCADE;
                """,
            """
                ALTER TABLE users_role ADD CONSTRAINT fk_users_role__role
                FOREIGN KEY (role_id) REFERENCES role(role_id) 
                ON UPDATE CASCADE ON DELETE CASCADE;
                """,
            """
                ALTER TABLE users_role ADD CONSTRAINT fk_users_role__user
                FOREIGN KEY (user_id) REFERENCES user(user_id) 
                ON UPDATE CASCADE ON DELETE CASCADE;
                """,
            """
                ALTER TABLE fleets_city ADD CONSTRAINT fk_fleets_city__city
                FOREIGN KEY (city_id) REFERENCES city(city_id) 
                ON UPDATE CASCADE ON DELETE CASCADE;
                """,
            """
                ALTER TABLE fleets_city ADD CONSTRAINT fk_fleets_city__fleet
                FOREIGN KEY (fleet_id) REFERENCES fleet(fleet_id) 
                ON UPDATE CASCADE ON DELETE CASCADE;
                """,
            """
                ALTER TABLE transport ADD CONSTRAINT fk_transport__fleet
                FOREIGN KEY (fleet_id) REFERENCES fleet(fleet_id) 
                ON UPDATE CASCADE ON DELETE CASCADE;
                """,
            """
                ALTER TABLE transport ADD CONSTRAINT fk_transport__kind
                FOREIGN KEY (kind_id) REFERENCES transports_kind(kind_id) 
                ON UPDATE CASCADE ON DELETE CASCADE;
                """,
            """
                ALTER TABLE my_order ADD CONSTRAINT fk_my_order__customer
                FOREIGN KEY (customer_id) REFERENCES customer(customer_id) 
                ON UPDATE CASCADE ON DELETE CASCADE;
                """,
            """
                ALTER TABLE orders_transport ADD CONSTRAINT fk_orders_transport__transport
                FOREIGN KEY (transport_id) REFERENCES transport(transport_id) 
                ON UPDATE CASCADE ON DELETE CASCADE;
                """,
            """
                ALTER TABLE orders_transport ADD CONSTRAINT fk_orders_transport__my_order
                FOREIGN KEY (my_order_id) REFERENCES my_order(my_order_id) 
                ON UPDATE CASCADE ON DELETE CASCADE;
                """,
            """
                ALTER TABLE orders_service ADD CONSTRAINT fk_orders_service__my_order
                FOREIGN KEY (my_order_id) REFERENCES my_order(my_order_id) 
                ON UPDATE CASCADE ON DELETE CASCADE;
                """,
            """
                ALTER TABLE orders_service ADD CONSTRAINT fk_orders_service__service
                FOREIGN KEY (service_id) REFERENCES service(service_id) 
                ON UPDATE CASCADE ON DELETE CASCADE;
                """,
            """
                ALTER TABLE order_services_begin_city ADD CONSTRAINT fk_order_services_begin_city__orders_service
                FOREIGN KEY (orders_service_id) REFERENCES orders_service(orders_service_id) 
                ON UPDATE CASCADE ON DELETE CASCADE;
                """,
            """
                ALTER TABLE order_services_begin_city ADD CONSTRAINT fk_order_services_begin_city__city
                FOREIGN KEY (city_id) REFERENCES city(city_id)
                ON UPDATE CASCADE ON DELETE CASCADE;
                """,
            """
                ALTER TABLE order_services_end_city ADD CONSTRAINT fk_order_services_end_city__orders_service
                FOREIGN KEY (orders_service_id) REFERENCES orders_service(orders_service_id) 
                ON UPDATE CASCADE ON DELETE CASCADE;
                """,
            """
                ALTER TABLE order_services_end_city ADD CONSTRAINT fk_order_services_end_city__city
                FOREIGN KEY (city_id) REFERENCES city(city_id)
                ON UPDATE CASCADE ON DELETE CASCADE;
                """,
            """
                ALTER TABLE my_order ADD CONSTRAINT fk_my_order__stage
                FOREIGN KEY (stage_id) REFERENCES stage(stage_id)
                ON UPDATE CASCADE ON DELETE CASCADE;
                """,
            """
                ALTER TABLE my_order ADD CONSTRAINT fk_my_order__status
                FOREIGN KEY (status_id) REFERENCES status(status_id)
                ON UPDATE CASCADE ON DELETE CASCADE;
                """
        ]
        self.__create_constructions = [
            """
                CREATE TABLE IF NOT EXISTS stage (
                    stage_id INT PRIMARY KEY AUTO_INCREMENT,
                    title TEXT NOT NULL,
                    description TEXT
                ) ENGINE = InnoDB
                """, #stage
            """
                CREATE TABLE IF NOT EXISTS status (
                    status_id INT PRIMARY KEY AUTO_INCREMENT,
                    title TEXT NOT NULL,
                    description TEXT
                ) ENGINE = InnoDB
                """, #status
            """
                CREATE TABLE IF NOT EXISTS transports_kind (
                    kind_id INT PRIMARY KEY AUTO_INCREMENT,
                    description TEXT,
                    title TEXT NOT NULL,
                    lifting_capacity REAL NOT NULL,
                    volume REAL NOT NULL
                ) ENGINE = InnoDB
                """, #transports_kind
            """
                CREATE TABLE IF NOT EXISTS city (
                    city_id INT PRIMARY KEY AUTO_INCREMENT,
                    title TEXT NOT NULL
                ) ENGINE = InnoDB
                """, #city
            """
                CREATE TABLE IF NOT EXISTS role (
                    role_id INT PRIMARY KEY AUTO_INCREMENT,
                    title TEXT NOT NULL,
                    description TEXT
                ) ENGINE = InnoDB
                """, #role
            """
                CREATE TABLE IF NOT EXISTS user (
                    user_id INT PRIMARY KEY AUTO_INCREMENT,
                    login TEXT NOT NULL,
                    password TEXT NOT NULL,
                    email TEXT NOT NULL,
                    phone_number TEXT NOT NULL
                ) ENGINE = InnoDB
                """, #user
            """
                CREATE TABLE IF NOT EXISTS fleet (
                    fleet_id INT PRIMARY KEY AUTO_INCREMENT,
                    title TEXT NOT NULL,
                    description TEXT,
                    address TEXT NOT NULL,
                    square REAL NOT NULL,
                    stars_quantity INT
                ) ENGINE = InnoDB
                """, #fleet
            """
                CREATE TABLE IF NOT EXISTS service (
                    service_id INT PRIMARY KEY AUTO_INCREMENT,
                    title TEXT NOT NULL,
                    description TEXT,
                    cost_weight REAL NOT NULL,
                    cost_radius REAL NOT NULL
                ) ENGINE = InnoDB
                """, #service
            """
                CREATE TABLE IF NOT EXISTS customer (
                    customer_id INT PRIMARY KEY AUTO_INCREMENT,
                    user_id INT NOT NULL,
                    country TEXT NOT NULL,
                    street TEXT NOT NULL,
                    home_number INT NOT NULL,
                    flat_number INT,
                    lastname TEXT NOT NULL,
                    name TEXT NOT NULL,
                    middle_name TEXT NOT NULL 
                ) ENGINE = InnoDB
                """, #customer
            """
                CREATE TABLE IF NOT EXISTS customers_city (
                    customer_id INT NOT NULL,
                    city_id INT NOT NULL,
                    PRIMARY KEY(customer_id, city_id)
                ) ENGINE = InnoDB
                """, #customers_city
            """
                CREATE TABLE IF NOT EXISTS employee (
                            employee_id INT PRIMARY KEY AUTO_INCREMENT,
                            user_id INT NOT NULL,
                            passport_data TEXT NOT NULL,
                            salary REAL NOT NULL,
                            requirements TEXT, 
                            duties TEXT,
                            status_id INT
                        ) ENGINE = InnoDB
                """, #employee
            """
                CREATE TABLE IF NOT EXISTS users_role (
                  user_id INT NOT NULL,
                  role_id INT NOT NULL,
                  PRIMARY KEY(user_id, role_id) 
                ) ENGINE = InnoDB
                """, #users_role
            """
                CREATE TABLE IF NOT EXISTS fleets_city (
                  fleet_id INT NOT NULL,
                  city_id INT NOT NULL,
                  PRIMARY KEY(fleet_id, city_id) 
                ) ENGINE = InnoDB
                """, #fleets_city
            """
                CREATE TABLE IF NOT EXISTS transport (
                    transport_id INT PRIMARY KEY AUTO_INCREMENT,
                    kind_id INT NOT NULL,
                    fleet_id INT NOT NULL 
                ) ENGINE = InnoDB
                """, #transport
            """
                CREATE TABLE IF NOT EXISTS my_order (
                    my_order_id INT PRIMARY KEY AUTO_INCREMENT,
                    commissions DATE,
                    executions DATE,
                    customer_id INT NOT NULL,
                    operator_id INT,
                    courier_id INT,
                    stage_id INT,
                    status_id INT
                ) ENGINE = InnoDB
                """, #my_order
            """
                CREATE TABLE IF NOT EXISTS orders_transport (
                    transport_id INT NOT NULL,
                    my_order_id INT NOT NULL,
                    PRIMARY KEY(transport_id, my_order_id)
                ) ENGINE = InnoDB
                """, #orders_transport
            """
                CREATE TABLE IF NOT EXISTS orders_service (
                    orders_service_id INT PRIMARY KEY AUTO_INCREMENT,      
                    service_id INT NOT NULL,
                    my_order_id INT NOT NULL,
                    quantity_weight REAL NOT NULL,
                    quantity_radius REAL NOT NULL,
                    destinations_address TEXT NOT NULL,
                    departures_address TEXT NOT NULL,
                    total_cost REAL NOT NULL 
                ) ENGINE = InnoDB
                """, #orders_service
            """
                CREATE TABLE IF NOT EXISTS order_services_begin_city (
                      order_services_begin_city_id INT PRIMARY KEY AUTO_INCREMENT,
                      city_id INT NOT NULL,
                      orders_service_id INT NOT NULL
                    ) ENGINE = InnoDB
                """, #order_services_begin_city
            """
                CREATE TABLE IF NOT EXISTS order_services_end_city (
                      order_services_end_city_id INT PRIMARY KEY AUTO_INCREMENT,
                      city_id INT NOT NULL,
                      orders_service_id INT NOT NULL 
                    ) ENGINE = InnoDB
                """  #order_services_end_city
        ]

    def generate_database(self, title):
        self.__database = title
        self.__connection = self.__sql_pointer.connect_host()
        sql_create_database = 'CREATE DATABASE IF NOT EXISTS ' + self.__database
        self.__sql_pointer.create_database(self.__connection, sql_create_database)

    def delete_database(self, title):
        database = title
        self.__connection = self.__sql_pointer.connect_host()
        sql_delete_database = 'DROP DATABASE ' + database
        self.__sql_pointer.dalete_database(self.__connection, sql_delete_database)

    def create_tables(self):
        for i in range(len(self.__create_constructions)):
            self.__connection = self.__sql_pointer.connect_database(self.__database)
            self.__sql_pointer.execute_query(self.__connection, self.__create_constructions[i])

    def fill_tables(self):
        """
        I've prepared csv-files with data for each table,
        so it allows me to load the data quickly and store it separately
        """
        for p in range(len(self.tables_names)):
            with open('csv-files/' + self.tables_names[p] + '.csv', 'r', encoding='utf-8') as f:
                r = csv.reader(f, delimiter=';')
                my_lists = list(r)
                my_values = [tuple(i) for i in my_lists]
                self.__connection = self.__sql_pointer.connect_database(self.__database)
                self.__sql_pointer.inserting_many_records(self.__connection, self.__insert_constructions[p], my_values)
            self.__connection = self.__sql_pointer.connect_database(self.__database)
            collection = self.__sql_pointer.execute_read_query(self.__connection,
                                                               "SELECT * FROM " + self.tables_names[p]
                                                               )
            print(('*** ' + self.tables_names[p] + ' ***').center(100))
            if len(collection) == 0:
                print('Empty')
            for item in collection:
                print(item)
            print('-' * 100 + '\n')

    def delete_tables(self):
        for i in range(len(self.tables_names)):
            self.__connection = self.__sql_pointer.connect_database(self.__database)
            self.__sql_pointer.execute_query(self.__connection, "DROP TABLE " + self.tables_names[i])

    def add_foreign_keys(self):
        for i in range(len(self.__alter_constructions)):
            self.__connection = self.__sql_pointer.connect_database(self.__database)
            self.__sql_pointer.execute_query(self.__connection, self.__alter_constructions[i])

    def finish_program(self):
        try:
            self.__connection.close()
        except Error as e:
            pass

    def show_table(self, title):
        self.__connection = self.__sql_pointer.connect_database(self.__database)
        data = self.__sql_pointer.execute_read_query(self.__connection,
                                                     "SELECT * FROM " + title)
        print(title.center(100))
        for row in data:
            print(row)
        print('-' * 100)

    def perform_query(self, query):
        self.__connection = self.__sql_pointer.connect_database(self.__database)
        self.__sql_pointer.execute_query(self.__connection, query)

    def perform(self, query, data):
        self.__connection = self.__sql_pointer.connect_database(self.__database)
        self.__sql_pointer.execute_query_data(self.__connection, query, data)


def main():
    host = 'localhost'
    user = 'root'
    password = 'Qwerty084922052001'
    database = 'coursework'
    my_db = MyDatabase(host, user, password)
    my_db.delete_database(database)
    my_db.generate_database(database)
    my_db.create_tables()
    my_db.fill_tables()
    my_db.add_foreign_keys()
    for i in my_db.tables_names:
        my_db.show_table(i)

    my_db.finish_program()


if __name__ == '__main__':
    main()