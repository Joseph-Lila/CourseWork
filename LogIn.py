from kivy.properties import ObjectProperty
from kivymd.uix.screen import MDScreen
from ChooseRole import ChooseRole
from Notification import Notification
from User import User
from DbOperator import DbOperator


class LogIn(MDScreen):
    my_login = ObjectProperty(None)
    my_password = ObjectProperty(None)
    dialog = None
    note = Notification(dialog)

    # If user login successfully, static field of class User contains his user_id

    def __refresh_fields(self):
        self.my_login.text = ''
        self.my_password.text = ''

    def button_login(self):
        if not DbOperator().try_connection():
            self.note.universal_note('Отсутствует соединение с одной из БД!', [])
            return
        if self.my_password.text == '' or self.my_login.text == '':
            self.note.universal_note('Не все поля заполнены!', [self.my_login, self.my_password])
            return
        User.user_id = DbOperator().get_user_id_with_login_and_password(self.my_login.text, self.my_password.text)
        if User.user_id == -1:
            self.note.universal_note('Такого пользователя в системе нет!', [self.my_login, self.my_password])
            return
        user_roles = DbOperator().get_user_roles_with_users_id(User.user_id)
        if len(user_roles) == 0:
            return
        self.__choose_role(user_roles)

    def dialog_close(self, *args):
        self.dialog.dismiss(force=True)

    # User is free to have few roles, so, here program's mechanism suggest what to do.
    # If user has only one role (CUSTOMER), he immediately gets customer's screen,
    # otherwise he get a choice.

    def __choose_role(self, user_roles):
        if len(user_roles) == 1:
            self.__refresh_fields()
            self.manager.current = 'customer'
        else:
            for item in user_roles:
                ChooseRole.buttons[item].disabled = False
            self.__refresh_fields()
            self.manager.current = 'choose_role'
