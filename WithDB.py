from MySQL import MySQL


class WithDB:

    def __init__(self):
        self.db_title = 'coursework'
        self.sql_pointer = MySQL('localhost', 'root', 'Qwerty084922052001')
        self.connection = None
        self.queries = {'get_user_id_with_login_and_password':
                        """
                        SELECT
                            user_id 
                        FROM 
                            user
                        WHERE
                            login = \"%s\" AND password = \"%s\" 
                        """,
                        'get_role_id_with_user_id':
                        """
                        SELECT
                        role_id
                        FROM
                        users_role
                        WHERE user_id = %s
                        """,
                        'get_role_title_with_role_id':
                        """
                        SELECT title
                        FROM
                        role
                        WHERE role_id = %s
                        """,
                        'get_user_id_with_phone_and_email':
                        """
                        SELECT user_id
                        FROM
                        user
                        WHERE phone = \"%s\" AND email = \"%s\"
                        """,
                        'get_role_id_with_role_title':
                        """
                        SELECT role_id
                        FROM role
                        WHERE title = \"%s\"                        
                        """,
                        'insert_stage':
                        """INSERT INTO stage (  
                            title, 
                            description 
                        ) 
                        VALUES ( \"%s\", \"%s\" )
                        """,
                        'insert_status':
                        """INSERT INTO status (  
                            title, 
                            description 
                        ) 
                        VALUES ( \"%s\", \"%s\" )
                        """,
                        'insert_transports_kind':
                        """INSERT INTO transports_kind (  
                            title,
                            description, 
                            lifting_capacity, 
                            volume
                        ) 
                        VALUES ( \"%s\", \"%s\", %s, %s )
                        """,
                        'alter_transports_kind':
                        """
                        UPDATE transports_kind
                        SET title = \"%s\",
                        description = \"%s\",
                        lifting_capacity = %s,
                        volume = %s
                        WHERE kind_id = %s
                        """,
                        'insert_city':
                        """INSERT INTO city (   
                            title 
                        ) 
                        VALUES ( \"%s\" )
                        """,
                        'insert_role':
                        """INSERT INTO role ( 
                            title,
                            description
                        ) 
                        VALUES ( \"%s\", \"%s\" )
                        """,
                        'insert_user':
                        """INSERT INTO user ( 
                            login,
                            password,
                            email,
                            phone_number
                        ) 
                        VALUES ( \"%s\", \"%s\", \"%s\", \"%s\" )
                        """,
                        'insert_fleet':
                        """INSERT INTO fleet (  
                            title, 
                            description, 
                            address,
                            square,
                            stars_quantity
                        ) 
                        VALUES ( \"%s\", \"%s\", \"%s\", %s, %s )
                        """,
                        'alter_fleet':
                        """
                        UPDATE fleet
                        SET title = \"%s\",
                        description = \"%s\",
                        address = \"%s\",
                        square = %s,
                        stars_quantity = %s
                        WHERE fleet_id = %s
                        """,
                        'insert_service':
                        """INSERT INTO service (  
                            title, 
                            description, 
                            cost_weight, 
                            cost_radius
                        ) 
                        VALUES ( \"%s\", \"%s\", %s, %s )
                        """,
                        'alter_service':
                        """
                        UPDATE service
                        SET title = \"%s\",
                        description = \"%s\",
                        cost_weight = %s,
                        cost_radius = %s,
                        WHERE service_id = %s
                        """,
                        'insert_customer':
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
                        VALUES ( %s, \"%s\", \"%s\", %s, %s, \"%s\", \"%s\", \"%s\" )
                        """,
                        'insert_customers_city':
                        """INSERT INTO customers_city ( 
                            customer_id,
                            city_id
                        ) 
                        VALUES ( %s, %s )
                        """,
                        'insert_employee':
                        """INSERT INTO employee ( 
                            user_id,
                            passport_data,
                            salary,
                            requirements,
                            duties,
                            status_id
                        ) 
                        VALUES ( %s, \"%s\", %s, \"%s\", \"%s\", %s )
                        """,
                        'insert_users_role':
                        """INSERT INTO users_role ( 
                            user_id,
                            role_id
                        ) 
                        VALUES ( %s, %s )
                        """,
                        'insert_fleets_city':
                        """INSERT INTO fleets_city ( 
                            fleet_id,
                            city_id
                        ) 
                        VALUES ( %s, %s )
                        """,
                        'insert_transport':
                        """INSERT INTO transport ( 
                            kind_id,
                            fleet_id
                        ) 
                        VALUES ( %s, %s)
                        """,
                        'insert_my_order':
                        """INSERT INTO my_order ( 
                            commissions,
                            executions,
                            customer_id,
                            operator_id,
                            courier_id,
                            stage_id,
                            status_id
                        ) 
                        VALUES ( %s, %s, %s, %s, %s, %s, %s )
                        """,
                        'insert_my_orders_transport':
                        """INSERT INTO orders_transport ( 
                            transport_id,
                            my_order_id
                        ) 
                        VALUES ( %s, %s )
                        """,
                        'insert_my_orders_service':
                        """INSERT INTO orders_service ( 
                            service_id,
                            my_order_id,
                            quantity_weight,
                            quantity_radius,
                            destinations_address,
                            departures_address,
                            total_cost
                        ) 
                        VALUES ( %s, %s, %s, %s, \"%s\", \"%s\", %s )
                        """,
                        'get_my_orders_service_id':
                        """
                        SELECT orders_service_id
                        FROM orders_service
                        WHERE 
                        service_id = %s AND
                        my_order_id = %s AND
                        quantity_weight = %s AND
                        quantity_radius = %s AND
                        destinations_address = \"%s\" AND
                        departures_address = \"%s\" AND
                        total_cost = %s
                        """,
                        'insert_order_services_begin_city':
                        """INSERT INTO order_services_begin_city ( 
                            city_id,
                            orders_service_id
                        ) 
                        VALUES ( %s, %s )
                        """,
                        'insert_order_services_end_city':
                        """INSERT INTO order_services_end_city ( 
                            city_id,
                            orders_service_id
                        ) 
                        VALUES ( %s, %s )
                        """,
                        'get_city_id_with_city_title':
                        """
                        SELECT city_id FROM city WHERE title = \"%s\"
                        """,
                        'get_user_id_with_login':
                        """
                        SELECT user_id FROM user WHERE login = \"%s\"
                        """,
                        'get_customer_id_with_user_id':
                        """
                        SELECT customer_id FROM customer WHERE user_id = %s
                        """,
                        'delete_user_with_login':
                        """
                        DELETE FROM user WHERE login = \"%s\"
                        """,
                        'get_city_titles':
                        """
                        SELECT title FROM city
                        """,
                        'get_fleet_titles':
                        """
                        SELECT title FROM fleet
                        """,
                        'get_service_titles':
                        """
                        SELECT title FROM service
                        """,
                        'get_kind_titles':
                        """
                        SELECT title FROM transports_kind
                        """,
                        'delete_city_with_title':
                        """
                        DELETE FROM city WHERE title = \"%s\"
                        """,
                        'alter_city':
                        """
                        UPDATE city
                        SET title = \"%s\"
                        WHERE city_id = %s
                        """,
                        'get_city_with_title':
                        """
                        SELECT * FROM city WHERE title = \"%s\"
                        """,
                        'get_kind_with_title':
                        """
                        SELECT * FROM transports_kind WHERE title = \"%s\"
                        """,
                        'get_fleet_with_title':
                        """
                        SELECT * FROM fleet WHERE title = \"%s\"
                        """,
                        'get_service_with_title':
                        """
                        SELECT * FROM service WHERE title = \"%s\"
                        """,
                        'get_free_couriers':
                        """
                        SELECT 
                        user.user_id
                        FROM 
                        user
                        INNER JOIN users_role ON users_role.user_id = user.user_id 
                        INNER JOIN role ON users_role.role_id = role.role_id 
                        WHERE 
                        role.title = \"Курьер\"
                        """,
                        'get_services_costs_with_title':
                        """
                        SELECT 
                        cost_weight, cost_radius
                        FROM
                        service
                        WHERE 
                        title = \"%s\"
                        """,
                        'add_order':
                        """INSERT INTO my_order ( 
                            commissions,
                            customer_id,
                            stage_id,
                            status_id
                        ) 
                        VALUES ( \"%s\", %s, %s, %s )
                        """,
                        'get_last_orders_id':
                        """
                        SELECT
                        my_order_id
                        FROM
                        my_order
                        WHERE
                        commissions = \"%s\" AND
                        executions IS NULL AND
                        customer_id = %s AND
                        operator_id IS NULL AND
                        courier_id IS NULL AND
                        stage_id = %s AND
                        status_id = %s
                        """,
                        'add_courier_id_and_operator_id_into_order_with_order_id':
                        """
                        UPDATE my_order
                        SET 
                        courier_id = %s, operator_id = %s, stage_id = %s
                        WHERE my_order_id = %s
                        """,
                        'alter_orders_status_id_with_order_id':
                        """
                        UPDATE my_order
                        SET status_id = %s
                        WHERE my_order_id = %s
                        """,
                        'add_orders_executions_and_stage_id_with_order_id':
                        """
                        UPDATE my_order
                        SET
                        executions = \"%s\", stage_id = %s
                        WHERE my_order_id = %s
                        """,
                        'alter_orders_stage_id_with_order_id':
                        """
                        UPDATE my_order
                        SET stage_id = %s
                        WHERE my_order_id = %s
                        """,
                        'get_stage_id_with_stage_title':
                        """
                        SELECT
                        stage_id
                        FROM
                        stage
                        WHERE title = \"%s\"
                        """,
                        'get_status_id_with_status_title':
                        """
                        SELECT
                        status_id
                        FROM
                        status
                        WHERE title = \"%s\"
                        """,
                        'get_active_orders_data_for_customer_with_customer_id':
                        """
                        SELECT
                        my_order.my_order_id,
                        my_order.commissions,
                        my_order.executions,
                        status.title,
                        stage.title
                        FROM 
                        my_order
                        INNER JOIN status ON status.status_id = my_order.status_id
                        INNER JOIN stage ON stage.stage_id = my_order.stage_id
                        WHERE 
                        (stage.title = \"На рассмотрении\" OR 
                        stage.title = \"Выполняется\") AND
                        my_order.customer_id = %s
                        """,
                        'get_passive_orders_data_for_customer_with_customer_id':
                        """
                        SELECT
                        my_order.my_order_id,
                        my_order.commissions,
                        my_order.executions,
                        status.title,
                        stage.title
                        FROM 
                        my_order
                        INNER JOIN status ON status.status_id = my_order.status_id
                        INNER JOIN stage ON stage.stage_id = my_order.stage_id
                        WHERE 
                        (stage.title <> \"На рассмотрении\" AND 
                        stage.title <> \"Выполняется\") AND
                        my_order.customer_id = %s
                        """,
                        'get_paid_orders':
                        """
                        SELECT my_order.my_order_id
                        FROM 
                        my_order
                        INNER JOIN stage ON stage.stage_id = my_order.stage_id
                        INNER JOIN status ON status.status_id = my_order.status_id
                        WHERE 
                        stage.title = \"На рассмотрении\" AND status.title = \"Оплачен\"
                        """,
                        'get_order_with_courier_id':
                        """
                        SELECT my_order.my_order_id
                        FROM
                        my_order
                        INNER JOIN stage ON stage.stage_id = my_order.stage_id
                        WHERE
                        courier_id = %s AND 
                        stage.title <> \"Выполнен\"                        
                        """,
                        'get_sum_profit_for_each_month':
                        """
                        SELECT
                        my_order.executions, Sum(orders_service.total_cost)
                        FROM
                        my_order
                        INNER JOIN orders_service ON orders_service.my_order_id = my_order.my_order_id
                        GROUP BY my_order.executions
                        """,
                        'get_quantity_of_each_services_item':
                        """
                        SELECT Count(service.service_id)
                        FROM
                        service INNER JOIN
                        orders_service ON orders_service.service_id = service.service_id
                        ORDER BY service.service_id
                        """
                        }

    def __connect_db(self):
        self.connection = self.sql_pointer.connect_database(self.db_title)
        if self.connection is None:
            return False
        return True

    def get_smth(self, query_title, arguments, outcome):
        if not self.__connect_db():

            return False
        try:
            res = self.sql_pointer.execute_read_query(self.connection,
                                                      self.queries[query_title] % tuple(arguments)
                                                      )
            if res is not None:
                for i in range(len(res)):
                    outcome.append(res[i])
            return True
        except BaseException as e:
            return False

    def insert_delete_alter_smth(self, query_title, arguments):
        if not self.__connect_db():
            return False
        try:
            self.sql_pointer.execute_query(self.connection,
                                           self.queries[query_title] % tuple(arguments)
                                           )
            return True
        except BaseException as e:
            return False
