from kivy.properties import ObjectProperty
from kivymd.uix.screen import MDScreen

from Notification import Notification
from WithDB import WithDB


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
        db_pointer = WithDB()
        city_id = []
        if db_pointer.get_smth('get_city_id_with_city_title', [title.text], city_id):
            if len(city_id) == 0:
                self.note.universal_note('Извините, но указанный город не обслуживается нашей компанией!', [title])
                return False
        return True

    def __check_not_login(self, title):
        db_pointer = WithDB()
        user_id = []
        if db_pointer.get_smth('get_user_id_with_login', [title.text], user_id):
            if len(user_id) == 1:
                self.note.universal_note('Пользователь с указанным логином уже есть!', [title])
                return False
        return True

    def button_sign_up(self):
        db_pointer = WithDB()
        if (self.field_country.text == ''
                or self.field_city.text == ''
                or self.field_street.text == ''
                or self.filed_house.text == ''
                or self.field_flat.text == ''
                or self.surname.text == ''
                or self.user_name.text == ''
                or self.middle_name.text == ''
                or self.email.text == ''
                or self.phone.text == ''
                or self.login.text == ''
                or self.password1.text == ''
                or self.password2.text == ''):
            self.note.universal_note('Не все поля заполнены!', [])
            return None
        elif self.password1.text != self.password2.text:
            self.note.universal_note('Пароли не совпадают!',
                                     [self.password1, self.password2]
                                     )
            return None
        elif not self.__check_city(self.field_city):
            return None
        elif not self.__check_not_login(self.login):
            return None
        elif not self.__check_data():
            self.note.universal_note("""Пароль должен содрежать, как минимум, одну строчную и одну прописную буквы, а также цифру!""",
                                     [self.password1, self.password2]
                                     )
            return None
        else:
            if self.__sign_up(self.login.text,
                              self.password1.text,
                              self.email.text,
                              self.phone.text,
                              self.field_country.text,
                              self.field_city.text,
                              self.field_street.text,
                              self.filed_house.text,
                              self.field_flat.text,
                              self.surname.text,
                              self.user_name.text,
                              self.middle_name.text
                              ):
                self.note.universal_note('Регистрация прошла успешно!', [])
                self.manager.current = 'login'
            else:
                self.note.universal_note('Ошибка. Проверьте корректность введенных данных и проверьте состояние соединения с базой данных!', [])
                return None

    def __sign_up(self, login, password, email, phone_number, country, city,
                  street, home_number, flat_number, lastname, name, middle_name):
        if not self.__sign_up_check(login, password, email, phone_number, country, city,
                                    street, home_number, flat_number, lastname, name, middle_name):
            db_pointer = WithDB()
            db_pointer.insert_delete_alter_smth('delete_user_with_login', [login])
            return False
        return True

    @staticmethod
    def __sign_up_check(login, password, email, phone_number, country, city,
                        street, home_number, flat_number, lastname, name, middle_name):
        db_pointer = WithDB()
        check = db_pointer.insert_delete_alter_smth('insert_user',
                                                    [login,
                                                     password,
                                                     email,
                                                     phone_number
                                                     ]
                                                    )
        if check:
            user_id = []
            if not db_pointer.get_smth('get_user_id_with_login', [login], user_id):
                return False
            check = db_pointer.insert_delete_alter_smth('insert_customer',
                                                        [user_id[0][0],
                                                         country,
                                                         street,
                                                         home_number,
                                                         flat_number,
                                                         lastname,
                                                         name,
                                                         middle_name
                                                         ]
                                                        )
            if check:
                try:
                    customer_id = []
                    customers_city = []
                    if not db_pointer.get_smth('get_customer_id_with_user_id', [user_id[0][0]], customer_id):
                        return False
                    if not db_pointer.get_smth('get_city_id_with_city_title', [city], customers_city):
                        return False
                    check = db_pointer.insert_delete_alter_smth('insert_customers_city', [customer_id[0][0],
                                                                                          customers_city[0][0]
                                                                                          ]
                                                                )
                except:
                    print('MISTAKEEE!!!')
                    return False
                if check:
                    role_id = []
                    if not db_pointer.get_smth('get_role_id_with_role_title', ['Клиент'], role_id):
                        return False
                    check = db_pointer.insert_delete_alter_smth('insert_users_role',
                                                                [user_id[0][0],
                                                                 role_id[0][0],
                                                                 ]
                                                                )
                    return check
        return False
