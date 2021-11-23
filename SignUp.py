from kivy.properties import ObjectProperty
from kivymd.uix.screen import MDScreen

from Notification import Notification
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

    def __refresh_fields(self):
        self.field_country.text = ''
        self.field_city.text = ''
        self.field_street.text = ''
        self.filed_house.text = ''
        self.field_flat.text = ''
        self.surname.text = ''
        self.user_name.text = ''
        self.middle_name.text = ''
        self.email.text = ''
        self.phone.text = ''
        self.login.text = ''
        self.password1.text = ''
        self.password2.text = ''

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
        SignUpConstruction = namedtuple("SignUpConstruction", ['login', 'password', 'email', 'phone_number', 'country',
                                                               'city_title', 'street', 'home_number', 'flat_number',
                                                               'lastname', 'name', 'middle_name', 'role_title'
                                                               ]
                                        )
        sign_up_tuple = SignUpConstruction(login=self.login.text, password=self.password1.text, email=self.email.text,
                                           phone_number=self.phone.text, country=self.field_country.text,
                                           city_title=self.field_city.text, street=self.field_street.text,
                                           home_number=self.filed_house.text, flat_number=self.field_flat.text,
                                           lastname=self.surname.text, name=self.user_name.text,
                                           middle_name=self.middle_name.text, role_title='Клиент'
                                           )
        for value in sign_up_tuple:
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
            if self.__transaction_sign_up(sign_up_tuple):
                self.__refresh_fields()
                self.manager.current = 'login'

    def __transaction_sign_up(self, sign_up_tuple) -> bool:
        if not DbOperator().sign_up_transaction(sign_up_tuple):
            self.note.universal_note('Транзакция не прошла успешно.', [])
            return False
        else:
            self.note.universal_note('Транзакция прошла успешно.', [])
            return True

