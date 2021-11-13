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
    def get_role_id_with_role_title(self, title):
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
    def get_user_id_with_login(self, login):
        pass

    @abc.abstractmethod
    def confirm_changes(self):
        pass

    @abc.abstractmethod
    def get_customer_id_with_user_id(self, user_id):
        pass

    @abc.abstractmethod
    def get_city_id_with_city_title(self, title):
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