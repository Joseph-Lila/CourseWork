from kivy.properties import ObjectProperty
from kivymd.uix.screen import MDScreen
from ChooseRole import ChooseRole
from Notification import Notification
from User import User
from WithDB import WithDB


class LogIn(MDScreen):
    my_login = ObjectProperty(None)
    my_password = ObjectProperty(None)
    dialog = None
    note = Notification(dialog)

    # If user login successfully, static field of class User contains his user_id

    def button_login(self):
        db_pointer = WithDB()
        if self.my_password.text == '' or self.my_login.text == '':
            self.note.universal_note('Не все поля заполнены!', [])
            return False
        user_roles = []
        User.user_id = []
        if not db_pointer.get_smth('get_user_id_with_login_and_password',
                                   [self.my_login.text,
                                    self.my_password.text
                                    ],
                                   User.user_id
                                   ):
            self.note.universal_note('Ошибка запроса!', [])
            return False
        if len(User.user_id) == 0:
            self.note.universal_note('Такого пользователя в системе нет!', [])
            return False
        User.user_id = User.user_id[0][0]
        if not db_pointer.get_smth('get_role_id_with_user_id',
                                   [User.user_id
                                    ],
                                   user_roles):
            return False
        self.__choose_role(user_roles)

    def dialog_close(self, *args):
        self.dialog.dismiss(force=True)

    # User is free to have few roles, so, here program's mechanism sudgest what to do.
    # If user has only one role (CUSTOMER), he immediately get customer's screen,
    # otherwise he get a choice.

    def __choose_role(self, user_roles):
        if len(user_roles) == 0:
            self.my_password.text = ''
            self.note.universal_note('Неправильно введен либо пароль, либо логин',
                                     [self.my_password]
                                     )
        else:
            if len(user_roles) == 1:
                role_id = []
                if not WithDB().get_smth('get_role_id_with_role_title', ['Клиент'], role_id):
                    self.note.universal_note('Произошло обезличивание!', [])
                else:
                    User.current_role_id = role_id[0][0]
                self.manager.current = 'customer'
            else:
                db_pointer = WithDB()
                title = []
                for i in range(len(user_roles)):
                    if not db_pointer.get_smth('get_role_title_with_role_id', [user_roles[i][0]], title):
                        title = []
                        return None
                    ChooseRole.buttons[title[-1][0]].disabled = False
                self.manager.current = 'choose_role'

