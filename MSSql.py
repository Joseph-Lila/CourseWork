from datetime import datetime

from AnyBDInterface import AnyBDInterface
from DB_Recorder import db_recorder
import pyodbc

from User import User


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

    def __select_where(self, what_, from_, where_) -> list:
        try:
            connector = pyodbc.connect(self.__connect_str)
            self.cursor = connector.cursor()
            select_str = f"SELECT {what_} FROM {from_} WHERE {where_}"
            self.cursor.execute(select_str)
            ans = []
            for item in self.cursor:
                ans.append(item)
            self.cursor.close()
            return ans
        except:
            return []

    def __execute(self, execute_str):
        try:
            connector = pyodbc.connect(self.__connect_str, autocommit=False)
            connector.execute(execute_str)
            connector.commit()
            connector.close()
        except:
            pass

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
            return []

    def try_connection(self) -> bool:
        try:
            connector = pyodbc.connect(self.__connect_str)
            connector.close()
            return True
        except:
            return False

    def get_role_id_with_role_title(self, title) -> int:
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

    def check_exists_order_with_commissions_and_customer_id(self, commissions, customer_id) -> bool:
        results = self.__select_where("commissions, customer_id", "my_order",
                                      f"commissions = '{commissions}' AND customer_id = {customer_id}"
                                      )
        if len(results) == 0:
            return False
        return True

    def check_orders_executions_and_stage_id_with_order_id(self, order_id) -> tuple:
        results = self.__select_where("executions, stage_id", "my_order", f"my_order_id = {order_id}")
        if len(results) == 0:
            return tuple()
        return results[0]

    def get_customer_id_with_user_id(self, user_id) -> int:
        results = self.__select_where("customer_id", "customer", f"users_id = {user_id}")
        if len(results) == 0:
            return -1
        return results[0][0]

    def sign_up_transaction(self, sign_up_tuple) -> bool:
        sql = f"""
USE Coursework_MSSQL;
        
BEGIN TRANSACTION [SignUp]
        
BEGIN TRY
        
DECLARE @login varchar(50);
DECLARE @password varchar(50);
DECLARE @email varchar(50);
DECLARE @phone_number varchar(50);
DECLARE @country varchar(50);
DECLARE @street varchar(50);
DECLARE @home_number varchar(50);
DECLARE @flat_number varchar(50);
DECLARE @lastname varchar(50);
DECLARE @name varchar(50);
DECLARE @middle_name varchar(50);
DECLARE @city_title varchar(50);
DECLARE @role_title varchar(50);
DECLARE @user_id INT;
DECLARE @customer_id INT;
DECLARE @customers_city INT;
DECLARE @role_id iNT;
        
SET @login = '{sign_up_tuple.login}';
SET @password= '{sign_up_tuple.password}';
SET @email = '{sign_up_tuple.email}';
SET @phone_number = '{sign_up_tuple.phone_number}';
SET @country = '{sign_up_tuple.country}'; 
SET @street = '{sign_up_tuple.street}';
SET @home_number = {sign_up_tuple.home_number};
SET @flat_number = {sign_up_tuple.flat_number};
SET @lastname = '{sign_up_tuple.lastname}';
SET @name = '{sign_up_tuple.name}';
SET @middle_name = '{sign_up_tuple.middle_name}'; 
SET @city_title = '{sign_up_tuple.city_title}';
SET @role_title = '{sign_up_tuple.role_title}';

INSERT INTO users VALUES (@login, @password, @email, @phone_number);
        
SET @user_id = (SELECT [users_id]
                FROM [dbo].[users]
                WHERE [login] = @login);
        

        
INSERT INTO customer VALUES (@user_id, @country, @street, @home_number, @flat_number, @lastname, @name, @middle_name);        
        
SET @customer_id = (SELECT [customer_id]
                    FROM [dbo].[customer]
                    WHERE [users_id] = @user_id);
        
SET @customers_city = (SELECT [city_id]
                    FROM [dbo].[city]
                    WHERE [title] = @city_title);
        
INSERT INTO customers_city VALUES (@customer_id, @customers_city);
        
SET @role_id = (SELECT [role_id]
                FROM [dbo].[roles]
                WHERE [title] = @role_title);
        
INSERT INTO users_role VALUES (@user_id, @role_id);
        
COMMIT TRANSACTION [SignUp]
        
END TRY
BEGIN CATCH
ROLLBACK TRANSACTION [SignUp]
END CATCH
        """
        self.__execute(sql)
        return self.check_exists_user_with_login(sign_up_tuple.login)

    def order_completed_transaction(self, user_id) -> bool:
        sql = f"""
                USE Coursework_MSSQL;

                BEGIN TRANSACTION [order_completed]
                
                BEGIN TRY
                
                DECLARE @order_id int;
                DECLARE @now datetime;
                DECLARE @user_id int;
                DECLARE @courier_id int;
                DECLARE @stage_id int;
                DECLARE @status_id int;
                
                --set {user_id}
                SET @user_id = 1;
                
                SET @courier_id = (SELECT employee_id
                                  FROM employee
                                  WHERE users_id = @user_id);
                
                SET @order_id = (SELECT my_order_id
                                FROM my_order
                                JOIN
                                stage
                                ON stage.stage_id = my_order.stage_id
                                WHERE courier_id = @courier_id AND stage.title <> 'Выполнен');
                
                SET @now = GETDATE();
                
                SET @stage_id = (SELECT stage_id
                                FROM stage
                                WHERE title = 'Выполнен');
                
                UPDATE my_order
                    SET
                    executions = @now, stage_id = @stage_id
                    WHERE my_order_id = @order_id;
                
                SET @status_id = (SELECT status_id
                                 FROM statuses
                                 WHERE title = 'Свободен');
                
                UPDATE employee
                    SET
                    status_id = @status_id
                    WHERE
                    employee_id = @courier_id;
                
                COMMIT TRANSACTION [order_completed]
                
                END TRY
                BEGIN CATCH
                ROLLBACK TRANSACTION [order_completed]
                END CATCH
                """
        self.__execute(sql)
        return self.when_shall_i_be_free(user_id)

    def linking_transaction(self, operator_id, courier_id, order_id) -> bool:
        sql = f"""
                USE Coursework_MSSQL;

                BEGIN TRANSACTION [linking_transaction]
                
                BEGIN TRY
                
                DECLARE @order_id int;
                DECLARE @now datetime;
                DECLARE @courier_id int;
                DECLARE @operator_id int;
                DECLARE @stage_id int;
                DECLARE @status_id int;
                
                SET @operator_id = {operator_id};
                
                SET @courier_id = {courier_id};
                
                SET @order_id = {order_id};
                
                SET @stage_id = (SELECT stage_id
                                FROM stage
                                WHERE title = 'Выполняется');
                                
                UPDATE my_order
                    SET 
                    courier_id = @courier_id, operator_id = @operator_id, stage_id = @stage_id
                    WHERE my_order_id = @order_id;
                
                SET @status_id = (SELECT status_id
                    FROM statuses
                    WHERE title = 'Занят');
                
                UPDATE employee
                    SET
                    status_id = @status_id
                    WHERE
                    users_id = @courier_id;
                
                COMMIT TRANSACTION [linking_transaction]
                
                END TRY
                BEGIN CATCH
                ROLLBACK TRANSACTION [linking_transaction]
                END CATCH
                """
        self.__execute(sql)
        return self.check_courier_id_not_null_with_order_id(order_id)

    def refusing_transaction(self, order_id) -> bool:
        sql = f"""
                USE Coursework_MSSQL;

                BEGIN TRANSACTION [refusing_transaction]
                
                BEGIN TRY
                
                DECLARE @order_id int;
                DECLARE @now datetime;
                DECLARE @stage_id int;
                
                SET @order_id = {order_id};
                
                SET @stage_id = (SELECT stage_id
                                FROM stage
                                WHERE title = 'Отменен');
                
                SET @now = GETDATE()
                
                UPDATE my_order
                    SET
                    executions = @now, stage_id = @stage_id
                    WHERE my_order_id = @order_id;
                
                COMMIT TRANSACTION [refusing_transaction]
                
                END TRY
                BEGIN CATCH
                ROLLBACK TRANSACTION [refusing_transaction]
                END CATCH        
                """
        self.__execute(sql)
        return self.check_orders_executions_and_stage_id_with_order_id(order_id)[1] == self\
            .get_stage_id_with_stage_title('Отменен')

    def customer_order_transaction(self, customer_order_tuple) -> bool:
        date_time = datetime.today().strftime("%Y-%d-%m %H:%M:%S")
        sql = f"""
USE Coursework_MSSQL;
        
BEGIN TRANSACTION [CustomerOrder]
        
BEGIN TRY

DECLARE @stage_title varchar(50);
SET @stage_title = 'На рассмотрении';

DECLARE @status_title varchar(50);
SET @status_title = 'Не оплачен';

DECLARE @services_title varchar(50);
SET @services_title = '{customer_order_tuple.title}';

DECLARE @quantity_weight float;
SET @quantity_weight = {customer_order_tuple.weight.text};

DECLARE @quantity_radius float;
SET @quantity_radius = {customer_order_tuple.radius.text};

DECLARE @destinations_address varchar(50);
SET @destinations_address = '{customer_order_tuple.destination.text}';

DECLARE @departures_address varchar(50);
SET @departures_address = '{customer_order_tuple.departure.text}';

DECLARE @total_cost float;
SET @total_cost = {customer_order_tuple.total_cost.text};

DECLARE @begin_city_title varchar(50);
SET @begin_city_title = '{customer_order_tuple.begin_city.text}';

DECLARE @end_city_title varchar(50);
SET @end_city_title = '{customer_order_tuple.end_city.text}';

DECLARE @user_id int;
SET @user_id = {User.user_id};

DECLARE @now datetime;
DECLARE @customer_id int;
DECLARE @stage_id int;
DECLARE @status_id int;
DECLARE @orders_id int;
DECLARE @service_id int;
DECLARE @orders_service_id int;
DECLARE @begin_city_id int;
DECLARE @end_city_id int;
        
SET @now = '{date_time}';
SET @customer_id = (SELECT
                customer_id
                FROM
                customer
                WHERE
                users_id = @user_id
                );

SET @stage_id = (SELECT
             stage_id
             FROM 
             stage
             WHERE
             title = @stage_title
             );

SET @status_id = (SELECT
              status_id
              FROM
              statuses
              WHERE
              title = @status_title
              );

INSERT INTO my_order (commissions, customer_id, stage_id, status_id) 
VALUES (@now, @customer_id, @stage_id, @status_id);

SET @orders_id = (SELECT
              my_order_id
              FROM
              my_order
              WHERE
              commissions = @now AND executions IS NULL AND customer_id = @customer_id
              AND operator_id IS NULL AND courier_id IS NULL AND stage_id = @stage_id
              AND status_id = @status_id
              );
        
SET @service_id = (SELECT
               service_id
               FROM services
               WHERE title = @services_title
               );

INSERT INTO orders_service (service_id, my_order_id, quantity_weight, 
quantity_radius, destinations_address, departures_address, total_cost)
VALUES (@service_id, @orders_id, @quantity_weight, @quantity_radius,
@destinations_address, @departures_address, @total_cost);

SET @orders_service_id = (SELECT
                      orders_service_id
                      FROM
                      orders_service
                      WHERE
                      service_id = @service_id AND my_order_id = @orders_id
                      AND quantity_weight = @quantity_weight
                      AND quantity_radius = @quantity_radius
                      AND destinations_address = @destinations_address
                      AND departures_address = @departures_address
                      AND total_cost = @total_cost
                      );

SET @begin_city_id = (SELECT
                  city_id
                  FROM
                  city
                  WHERE
                  title = @begin_city_title
                  );

SET @end_city_id = (SELECT
                  city_id
                  FROM
                  city
                  WHERE
                  title = @end_city_title
                  );

INSERT INTO order_services_begin_city(city_id, orders_service_id)
VALUES (@begin_city_id, @orders_service_id);

INSERT INTO order_services_end_city(city_id, orders_service_id)
VALUES (@end_city_id, @orders_service_id);

COMMIT TRANSACTION [CustomerOrder]
        
END TRY
BEGIN CATCH
ROLLBACK TRANSACTION [CustomerOrder]
END CATCH
                """
        self.__execute(sql)
        return self.check_exists_order_with_commissions_and_customer_id(date_time,
                                                                        self.get_customer_id_with_user_id(User.user_id)
                                                                        )

    def get_services_costs_with_title(self, title) -> tuple:
        results = self.__select_where("cost_weight, cost_radius",
                                      "services",
                                      f"title = '{title}'"
                                      )
        if len(results) == 0:
            return ()
        return tuple([results[0][0], results[0][1]])

    def get_user_id_with_login_and_password(self, login, password) -> int:
        results = self.__select_where("users_id", "users", f"login = '{login}' AND password = '{password}'")
        if len(results) == 0:
            return -1
        return results[0][0]

    def get_user_roles_with_users_id(self, users_id) -> tuple:
        results = self.__select_where("title",
                                      """users
                                         JOIN users_role
                                         ON users.users_id = users_role.users_id
                                         JOIN roles
                                         ON roles.role_id = users_role.role_id""",
                                      f"users.users_id = {users_id}"
                                      )
        ans = tuple((item[0] for item in results))
        if len(ans) == 0:
            return ()
        return ans

    def get_city_titles(self) -> tuple:
        results = self.__select("title", "city")
        if len(results) == 0:
            return tuple()
        return tuple((item[0] for item in results))

    def get_fleet_titles(self) -> tuple:
        results = self.__select("title", "fleet")
        if len(results) == 0:
            return tuple()
        return tuple((item[0] for item in results))

    def get_kind_titles(self) -> tuple:
        results = self.__select("title", "transports_kind")
        if len(results) == 0:
            return tuple()
        return tuple((item[0] for item in results))

    def get_services_titles_and_total_costs(self) -> tuple:
        results = self.__select("services.title, SUM(total_cost) as total_cost",
                                """
                                services
                                JOIN 
                                orders_service
                                ON services.service_id = orders_service.service_id
                                GROUP BY services.title
                                """
                                )
        if len(results) == 0:
            return tuple()
        return tuple(results)

    def get_months_quantity_orders(self) -> tuple:
        results = self.__select("DATENAME(M, MONTH(commissions)) as months, COUNT(my_order_id) as quantity",
                                "my_order GROUP BY DATENAME(M, MONTH(commissions))")
        if len(results) == 0:
            return tuple()
        return tuple(results)

    def get_cities_quantity_orders(self) -> tuple:
        results = self.__select("city.title, COUNT(orders_service.orders_service_id) as quantity",
                                """
                                city
                                JOIN 
                                order_services_begin_city
                                ON city.city_id = order_services_begin_city.city_id
                                JOIN 
                                orders_service
                                ON order_services_begin_city.orders_service_id = orders_service.orders_service_id
                                GROUP BY city.title
                                """
                                )
        if len(results) == 0:
            return tuple()
        return tuple(results)

    def get_service_titles(self) -> tuple:
        results = self.__select("title", "services")
        if len(results) == 0:
            return tuple()
        return tuple((item[0] for item in results))

    def when_shall_i_be_free(self, user_id) -> bool:
        results = self.__select_where("users_id",
                                      """      
                                        employee
                                        JOIN statuses
                                        ON statuses.status_id = employee.status_id
                                        """,
                                      f"users_id = {user_id} AND statuses.title = 'Свободен'", )
        if len(results) == 0:
            return False
        return True

    def get_stage_id_with_stage_title(self, stage_title) -> int:
        results = self.__select_where("stage_id", "stage", f"title = '{stage_title}'")
        if len(results) == 0:
            return -1
        return results[0][0]

    def get_status_id_with_status_title(self, status_title) -> int:
        results = self.__select_where("status_id", "statuses", f"title = '{status_title}'")
        if len(results) == 0:
            return -1
        return results[0][0]

    def alter_orders_status_id_with_order_id(self, orders_status, order_id) -> bool:
        sql = f"""
                UPDATE my_order
                    SET status_id = {orders_status}
                    WHERE my_order_id = {order_id}
                """
        self.__execute(sql)
        return orders_status == self.check_orders_status_id_with_order_id(order_id)

    def get_passive_orders_data_for_customer_with_customer_id(self, customer_id) -> tuple:
        results = self.__select_where(
            "my_order_id, commissions, executions, statuses.title, stage.title",
            """my_order
                 JOIN statuses 
                 ON statuses.status_id = my_order.status_id
                 JOIN stage 
                 ON stage.stage_id = my_order.stage_id""",
            f"(stage.title <> 'На рассмотрении' AND stage.title <> 'Выполняется') AND customer_id = {customer_id}"
        )
        if len(results) == 0:
            return ()
        return tuple(results)

    def get_active_orders_data_for_customer_with_customer_id(self, customer_id) -> tuple:
        results = self.__select_where(
            "my_order_id, commissions, executions, statuses.title, stage.title",
            """my_order
                 JOIN statuses 
                 ON statuses.status_id = my_order.status_id
                 JOIN stage 
                 ON stage.stage_id = my_order.stage_id""",
            f"(stage.title = 'На рассмотрении' OR stage.title = 'Выполняется') AND customer_id = {customer_id}"
        )
        if len(results) == 0:
            return ()
        return tuple(results)

    def check_orders_status_id_with_order_id(self, order_id) -> int:
        results = self.__select_where("status_id", "my_order", f"my_order_id = {order_id}")
        if len(results) == 0:
            return -1
        return results[0][0]

    def check_courier_id_not_null_with_order_id(self, order_id) -> bool:
        results = self.__select_where("courier_id", 'my_order', f"my_order_id = {order_id}")
        if len(results) == 0:
            return False
        if results[0][0] is None:
            return False
        return True

    def get_free_couriers(self) -> tuple:
        results = self.__select("users.users_id",
                                """
                                users
                                JOIN
                                users_role
                                ON users_role.users_id = users.users_id
                                JOIN
                                roles
                                ON users_role.role_id = roles.role_id
                                JOIN 
                                employee
                                ON employee.users_id = users.users_id
                                JOIN
                                statuses
                                ON statuses.status_id = employee.status_id
                                WHERE
                                roles.title = 'Курьер' AND statuses.title = 'Свободен'
                                """
                                )
        if len(results) == 0:
            return tuple()
        return tuple((item[0] for item in results))

    def get_paid_orders(self) -> tuple:
        results = self.__select("my_order.my_order_id",
                                """
                                my_order
                                JOIN
                                stage
                                ON stage.stage_id = my_order.stage_id
                                JOIN
                                statuses
                                ON statuses.status_id = my_order.status_id
                                WHERE
                                stage.title = 'На рассмотрении' AND statuses.title = 'Оплачен'
                                """
                                )
        if len(results) == 0:
            return tuple()
        return tuple((item[0] for item in results))

    def get_city_fields_with_title(self, title) -> tuple:
        result = self.__select_where("*", "city", f"title = '{title}'")
        if len(result) == 0:
            return tuple()
        return result[-1]

    def get_fleet_fields_with_title(self, title) -> tuple:
        result = self.__select_where("*", "fleet", f"title = '{title}'")
        if len(result) == 0:
            return tuple()
        return result[-1]

    def get_kind_fields_with_title(self, title) -> tuple:
        result = self.__select_where("*", "transports_kind", f"title = '{title}'")
        if len(result) == 0:
            return tuple()
        return result[-1]

    def get_service_fields_with_title(self, title) -> tuple:
        result = self.__select_where("*", "services", f"title = '{title}'")
        if len(result) == 0:
            return tuple()
        return result[-1]

    def alter_city_using_str_collection(self, data):
        sql = f"""
                UPDATE city
                SET
                title = '{data[1]}'
                WHERE
                city_id = {int(data[0])}
                """
        self.__execute(sql)

    def alter_fleet_using_str_collection(self, data):
        sql = f"""
                        UPDATE fleet
                        SET
                        title = '{data[1]}',
                        description = '{data[2]}',
                        address = '{data[3]}',
                        square = {float(data[4])},
                        stars_quantity = {int(data[5])}
                        WHERE
                        fleet_id = {int(data[0])}
                        """
        self.__execute(sql)

    def alter_kind_using_str_collection(self, data):
        sql = f"""
                                UPDATE transports_kind
                                SET
                                description = '{data[1]}',
                                title = '{data[2]}',
                                lifting_capacity = {float(data[3])},
                                volume = {float(data[4])}
                                WHERE
                                kind_id = {int(data[0])}
                                """
        self.__execute(sql)

    def alter_service_using_str_collection(self, data):
        sql = f"""
                                        UPDATE services
                                        SET
                                        title = '{data[1]}',
                                        description = '{data[2]}',
                                        cost_weight = {float(data[3])},
                                        cost_radius = {float(data[4])}
                                        WHERE
                                        kind_id = {int(data[0])}
                                        """
        self.__execute(sql)
