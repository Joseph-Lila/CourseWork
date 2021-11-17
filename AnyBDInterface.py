import abc


class AnyBDInterface(abc.ABC):

    @abc.abstractmethod
    def try_connection(self) -> bool:
        pass

    @abc.abstractmethod
    def get_role_id_with_role_title(self, title: list) -> tuple:
        pass

    @abc.abstractmethod
    def check_exists_user_with_login(self, login: list) -> bool:
        pass

    @abc.abstractmethod
    def check_exists_city_with_title(self, title: list) -> bool:
        pass

    @abc.abstractmethod
    def get_customer_id_with_user_id(self, user_id: list) -> int:
        pass

    @abc.abstractmethod
    def sign_up_transaction(self, sign_up_tuple: list) -> bool:
        pass

    @abc.abstractmethod
    def order_completed_transaction(self, user_id: list) -> bool:
        pass

    @abc.abstractmethod
    def refusing_transaction(self, order_id: list) -> bool:
        pass

    @abc.abstractmethod
    def when_shall_i_be_free(self, user_id: list) -> bool:
        pass

    @abc.abstractmethod
    def customer_order_transaction(self, customer_order_tuple: list) -> bool:
        pass

    @abc.abstractmethod
    def get_user_id_with_login_and_password(self, login: list, password: list) -> tuple:
        pass

    @abc.abstractmethod
    def get_user_roles_with_users_id(self, users_id: list) -> tuple:
        pass

    @abc.abstractmethod
    def get_stage_id_with_stage_title(self, stage_title: list) -> int:
        pass

    @abc.abstractmethod
    def get_status_id_with_status_title(self, status_title: list) -> int:
        pass

    @abc.abstractmethod
    def alter_orders_status_id_with_order_id(self, orders_status: list, order_id: list) -> bool:
        pass

    @abc.abstractmethod
    def check_orders_executions_and_stage_id_with_order_id(self, order_id: list) -> tuple:
        pass

    @abc.abstractmethod
    def check_orders_status_id_with_order_id(self, order_id: list) -> int:
        pass

    @abc.abstractmethod
    def get_passive_orders_data_for_customer_with_customer_id(self, customer_id: list) -> tuple:
        pass

    @abc.abstractmethod
    def get_active_orders_data_for_customer_with_customer_id(self, customer_id: list) -> tuple:
        pass

    @abc.abstractmethod
    def get_services_costs_with_title(self, title: list) -> tuple:
        pass

    @abc.abstractmethod
    def get_city_titles(self) -> tuple:
        pass

    @abc.abstractmethod
    def check_exists_order_with_commissions_and_customer_id(self, commissions: list, customer_id: list) -> bool:
        pass

    @abc.abstractmethod
    def get_service_titles(self) -> tuple:
        pass

    @abc.abstractmethod
    def check_courier_id_not_null_with_order_id(self, order_id: list) -> bool:
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
    def get_city_fields_with_title(self, title: list) -> tuple:
        pass

    @abc.abstractmethod
    def get_service_fields_with_title(self, title: list) -> tuple:
        pass

    @abc.abstractmethod
    def get_kind_fields_with_title(self, title: list) -> tuple:
        pass

    @abc.abstractmethod
    def get_fleet_fields_with_title(self, title: list) -> tuple:
        pass

    @abc.abstractmethod
    def alter_city_using_str_collection(self, data: list):
        pass

    @abc.abstractmethod
    def alter_service_using_str_collection(self, data: list):
        pass

    @abc.abstractmethod
    def alter_kind_using_str_collection(self, data: list):
        pass

    @abc.abstractmethod
    def alter_fleet_using_str_collection(self, data: list):
        pass

    @abc.abstractmethod
    def linking_transaction(self, operator_id: list, courier_id: list, order_id: list) -> bool:
        pass
