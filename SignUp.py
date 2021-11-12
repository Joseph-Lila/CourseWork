from kivy.properties import ObjectProperty
from kivymd.uix.screen import MDScreen

from Notification import Notification
from DB_Recorder import db_representatives
from collections import namedtuple
from DbOperator import DbOperator


class SignUp(MDScreen):
    field_country = ObjectProperty(None)
    field_city = ObjectProperty(None)
    field_street = ObjectProperty(None)
    filed_house = ObjectProperty(None)
    field_flat = ObjectProperty(None)
    surname = ObjectProperty(None)
    user_name = ObjectProperty(None)
    middle_name = ObjectProperty(None)
    email = ObjectProperty(None)
    phone = ObjectProperty(None)
    login = ObjectProperty(None)
    password1 = ObjectProperty(None)
    password2 = ObjectProperty(None)
    check_box = ObjectProperty(None)
    last_btn = ObjectProperty(None)
    dialog = None
    note = Notification(dialog)

    def dialog_close(self, *args):
        self.dialog.dismiss(force=True)

    def on_checkbox_active(self):
        if self.check_box.active:
            self.last_btn.disabled = False
        else:
            self.last_btn.disabled = True

    def __check_data(self):
        up_symbol = False
        low_symbol = False
        number = False
        for i in self.password1.text:
            if i.islower():
                low_symbol = True
        for i in self.password1.text:
            if i.isupper():
                up_symbol = True
        for i in self.password1.text:
            if i.isdigit():
                number = True
        return up_symbol and low_symbol and number

    def __check_city(self, title):
        if not DbOperator().check_exists_city_with_title(title.text):
            self.note.universal_note('Компания не обслуживает указанный город!', [title])
            return False
        return True

    def __check_not_login(self, title):
        if DbOperator().check_exists_user_with_login(title.text):
            self.note.universal_note('Пользователь с указанным логином уже есть!', [title])
            return False
        return True

    def button_sign_up(self):
        if not DbOperator().try_connection():
            self.note.universal_note('Отсутствует соединение с одной из БД!', [])
            return False
        SignUpForm = namedtuple(
            "SignUpForm",
            [
                'login',
                'password',
                'email',
                'phone_number',
                'country',
                'city',
                'street',
                'home_number',
                'flat_number',
                'lastname',
                'name',
                'middle_name',
            ]
        )
        fields = SignUpForm(
            login=self.login.text,
            password=self.password1.text,
            email=self.email.text,
            phone_number=self.phone.text,
            country=self.field_country.text,
            city=self.field_city.text,
            street=self.field_street.text,
            home_number=self.filed_house.text,
            flat_number=self.field_flat.text,
            lastname=self.surname.text,
            name=self.user_name.text,
            middle_name=self.middle_name.text
        )
        for value in fields:
            if value == '':
                self.note.universal_note('Не все поля заполнены!', [])
                return None
        if self.password1.text != self.password2.text:
            self.note.universal_note('Пароли не совпадают!', [self.password1, self.password2])
        elif not self.__check_city(self.field_city):
            return None
        elif not self.__check_not_login(self.login):
            return None
        elif not self.__check_data():
            self.note.universal_note(
                """Пароль должен содрежать, как минимум, одну строчную и одну прописную буквы, а также цифру!""",
                [self.password1, self.password2]
            )
            return None
        else:
            if self.__sign_up(fields):
                self.note.universal_note('Регистрация прошла успешно!', [])
                self.manager.current = 'login'
            else:
                self.note.universal_note(
                    'Ошибка. Проверьте корректность введенных данных и проверьте состояние соединения с базой данных!',
                    []
                )
                return None

    def __sign_up(self, fields):
        if not self.__sign_up_check(fields):
            if not DbOperator().delete_user_with_login(fields.login):
                self.note.universal_note('Критическая ошибка!\nСвяжитесь с администратором.',
                                         [self.password1, self.password2]
                                         )
            return False
        return True

    @staticmethod
    def __sign_up_check(fields):
        if DbOperator().create_user(
                fields.login,
                fields.password,
                fields.email,
                fields.phone_number
        ):
            print("user eas created")
            user_id = DbOperator().get_user_id_with_login(fields.login)
            if user_id is None:
                return False
            if DbOperator().create_customer([user_id, fields.country, fields.street, fields.home_number,
                                             fields.flat_number, fields.lastname, fields.name, fields.middle_name]):
                print("customer was created")
                customer_id = DbOperator().get_customer_id_with_user_id(user_id)
                customers_city = DbOperator().get_city_id_with_city_title(fields.city)
                if customer_id is None or customers_city is None:
                    return False
                if DbOperator().insert_customers_city(customer_id, customers_city):
                    print("customers_city was created")
                    role_id = DbOperator().get_role_id_with_role_title('Клиент')
                    if role_id is None:
                        return None
                    return DbOperator().insert_users_role(user_id, role_id)
        return False
