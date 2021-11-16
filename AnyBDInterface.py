import abc


class AnyBDInterface(abc.ABC):

    @abc.abstractmethod
    def try_connection(self) -> bool:
        pass

    @abc.abstractmethod
    def create_customer(self, data_collection) -> bool:
        """
        This method allows creating customer using inputted data.
        """

    @abc.abstractmethod
    def create_user(self, login, password, email, phone_number) -> bool:
        pass

    @abc.abstractmethod
    def get_role_id_with_role_title(self, title) -> int:
        pass

    @abc.abstractmethod
    def check_exists_user_with_login(self, login) -> bool:
        pass

    @abc.abstractmethod
    def check_exists_city_with_title(self, title) -> bool:
        pass

    @abc.abstractmethod
    def delete_user_with_login(self, login) -> bool:
        pass

    @abc.abstractmethod
    def get_user_id_with_login(self, login) -> int:
        pass

    @abc.abstractmethod
    def confirm_changes(self):
        pass

    @abc.abstractmethod
    def get_customer_id_with_user_id(self, user_id) -> int:
        pass

    @abc.abstractmethod
    def get_city_id_with_city_title(self, title) -> int:
        pass

    @abc.abstractmethod
    def insert_customers_city(self, customer_id, city_id) -> bool:
        pass

    @abc.abstractmethod
    def insert_users_role(self, user_id, role_id) -> bool:
        pass

    @abc.abstractmethod
    def sign_up_transaction(self, sign_up_tuple) -> bool:
        pass

    @abc.abstractmethod
    def customer_order_transaction(self, customer_order_tuple) -> bool:
        pass

    @abc.abstractmethod
    def get_user_id_with_login_and_password(self, login, password) -> int:
        pass

    @abc.abstractmethod
    def get_user_roles_with_users_id(self, users_id) -> tuple:
        pass

    @abc.abstractmethod
    def get_order_id_with_courier_id(self, courier_id) -> int:
        pass

    @abc.abstractmethod
    def get_stage_id_with_stage_title(self, stage_title) -> int:
        pass

    @abc.abstractmethod
    def get_status_id_with_status_title(self, status_title) -> int:
        pass

    @abc.abstractmethod
    def add_orders_executions_and_stage_id_with_order_id(self, orders_executions, stage_id, order_id) -> bool:
        pass

    @abc.abstractmethod
    def alter_orders_status_id_with_order_id(self, orders_status, order_id) -> bool:
        pass

    @abc.abstractmethod
    def check_orders_executions_and_stage_id_with_order_id(self, order_id) -> tuple:
        pass

    @abc.abstractmethod
    def check_orders_status_id_with_order_id(self, order_id) -> int:
        pass

    @abc.abstractmethod
    def get_passive_orders_data_for_customer_with_customer_id(self, customer_id) -> tuple:
        pass

    @abc.abstractmethod
    def get_active_orders_data_for_customer_with_customer_id(self, customer_id) -> tuple:
        pass

    @abc.abstractmethod
    def get_services_costs_with_title(self, title) -> tuple:
        pass

    @abc.abstractmethod
    def change_courier_status(self, courier_id, status) -> bool:
        pass

    @abc.abstractmethod
    def get_courier_status_id(self, courier_id) -> int:
        pass

    @abc.abstractmethod
    def get_city_titles(self) -> tuple:
        pass

    @abc.abstractmethod
    def check_exists_order_with_commissions_and_customer_id(self, commissions, customer_id) -> bool:
        pass

    @abc.abstractmethod
    def get_service_titles(self) -> tuple:
        pass

    @abc.abstractmethod
    def add_courier_id_and_operator_id_into_order_with_order_id(self,
                                                                courier_id,
                                                                operator_id,
                                                                stage_id,
                                                                order_id
                                                                ) -> bool:
        pass

    @abc.abstractmethod
    def check_courier_id_not_null_with_order_id(self, order_id) -> bool:
        pass

    @abc.abstractmethod
    def get_free_couriers(self) -> tuple:
        pass

    @abc.abstractmethod
    def get_paid_orders(self) -> tuple:
        pass

    @abc.abstractmethod
    def get_services_titles_and_total_costs(self) -> tuple:
        pass

    @abc.abstractmethod
    def get_months_quantity_orders(self) -> tuple:
        pass

    @abc.abstractmethod
    def get_cities_quantity_orders(self) -> tuple:
        pass

    @abc.abstractmethod
    def get_fleet_titles(self) -> tuple:
        pass

    @abc.abstractmethod
    def get_kind_titles(self) -> tuple:
        pass

    @abc.abstractmethod
    def get_city_fields_with_title(self, title) -> tuple:
        pass

    @abc.abstractmethod
    def get_service_fields_with_title(self, title) -> tuple:
        pass

    @abc.abstractmethod
    def get_kind_fields_with_title(self, title) -> tuple:
        pass

    @abc.abstractmethod
    def get_fleet_fields_with_title(self, title) -> tuple:
        pass

    @abc.abstractmethod
    def alter_city_using_str_collection(self, data):
        pass

    @abc.abstractmethod
    def alter_service_using_str_collection(self, data):
        pass

    @abc.abstractmethod
    def alter_kind_using_str_collection(self, data):
        pass

    @abc.abstractmethod
    def alter_fleet_using_str_collection(self, data):
        pass
