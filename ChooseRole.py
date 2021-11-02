from kivy.app import App
from kivy.uix.anchorlayout import AnchorLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.widget import Widget
from kivymd.uix.button import MDFillRoundFlatButton, MDIconButton
from kivymd.uix.card import MDCard
from kivymd.uix.screen import MDScreen

from Notification import Notification
from User import User
from WithDB import WithDB


class ChooseRole(MDScreen):
    """
    Here there are from 2 up to 4 special buttons. It depends on user's roles quantity.
    So, It would be good to create flexible screen.
    """
    buttons = {"Курьер": 0,
               "Клиент": 0,
               "Оператор": 0,
               "Директор": 0
               }
    dialog = None
    note = Notification(dialog)

    def __init__(self, **kw):
        super(ChooseRole, self).__init__(**kw)
        self.md_bg_color = [40 / 255, 40 / 255, 180 / 255, 80 / 255]
        self.add_buttons()

    def add_buttons(self):
        main_container = self.__main_container()
        main_container.add_widget(self.__icons())
        main_container.add_widget(Widget())
        self.buttons["Клиент"] = self.__button_customer()
        self.buttons['Курьер'] = self.__button_courier()
        self.buttons['Оператор'] = self.__button_operator()
        self.buttons['Директор'] = self.__button_director()
        for val in self.buttons.values():
            main_container.add_widget(val)
        main_container.add_widget(Widget())
        self.add_widget(main_container)

    @staticmethod
    def __main_container():
        main_container = MDCard()
        main_container.size_hint = (.7, .8)
        main_container.pos_hint = {"center_x": .5, "center_y": .5}
        main_container.elevation = 15
        main_container.padding = 20
        main_container.spacing = 60
        main_container.orientation = 'vertical'
        main_container.md_bg_color = [10 / 255, 10 / 255, 140 / 255, 100 / 255]
        return main_container

    def __icons(self):
        main_cont = GridLayout()
        main_cont.valign = 'center'
        main_cont.cols = 2
        main_cont.rows = None
        anch1 = AnchorLayout()
        anch2 = AnchorLayout()
        first_icon_button = MDIconButton()
        second_icon_button = MDIconButton()
        first_icon_button.user_font_size = '30sp'
        second_icon_button.user_font_size = '30sp'
        first_icon_button.icon_color = [1, 1, 1, 1]
        second_icon_button.icon_color = [1, 1, 1, 1]
        first_icon_button.icon = 'arrow-left'
        second_icon_button.icon = 'door'
        first_icon_button.md_bg_color = [10 / 255, 10 / 255, 140 / 255, 255 / 255]
        second_icon_button.md_bg_color = [10 / 255, 10 / 255, 140 / 255, 255 / 255]
        first_icon_button.bind(on_press=self.go_to_login)
        second_icon_button.bind(on_press=App.get_running_app().stop)
        anch1.add_widget(first_icon_button)
        anch2.add_widget(second_icon_button)
        main_cont.add_widget(anch1)
        main_cont.add_widget(anch2)
        return main_cont

    def go_to_login(self, *args):
        self.manager.current = 'login'

    def __button_customer(self):
        button = MDFillRoundFlatButton()
        button.disabled = True
        button.pos_hint = {"center_x": .5}
        button.font_size = 15
        button.md_bg_color = [10 / 255, 10 / 255, 140 / 255, 100 / 255]
        button.text_color = [1, 1, 1, 1]
        button.text = 'Клиент'
        button.bind(on_press=self.customer)
        return button

    def __button_courier(self):
        button = MDFillRoundFlatButton()
        button.disabled = True
        button.pos_hint = {"center_x": .5}
        button.font_size = 15
        button.md_bg_color = [10 / 255, 10 / 255, 140 / 255, 100 / 255]
        button.text_color = [1, 1, 1, 1]
        button.text = 'Курьер'
        button.bind(on_press=self.courier)
        return button

    def __button_operator(self):
        button = MDFillRoundFlatButton()
        button.disabled = True
        button.pos_hint = {"center_x": .5}
        button.font_size = 15
        button.md_bg_color = [10 / 255, 10 / 255, 140 / 255, 100 / 255]
        button.text_color = [1, 1, 1, 1]
        button.text = 'Оператор'
        button.bind(on_press=self.operator)
        return button

    def __button_director(self):
        button = MDFillRoundFlatButton()
        button.disabled = True
        button.pos_hint = {"center_x": .5}
        button.font_size = 15
        button.md_bg_color = [10 / 255, 10 / 255, 140 / 255, 100 / 255]
        button.text_color = [1, 1, 1, 1]
        button.text = 'Директор'
        button.bind(on_press=self.director)
        return button

    def customer(self, *args):

        role_id = []
        if not WithDB().get_smth('get_role_id_with_role_title', ['Клиент'], role_id):
            self.note.universal_note('Произошло обезличивание!', [])
        else:
            User.current_role_id = role_id[0]
        self.manager.current = 'customer'

    def courier(self, *args):
        role_id = []
        if not WithDB().get_smth('get_role_id_with_role_title', ['Курьер'], role_id):
            self.note.universal_note('Произошло обезличивание!', [])
        else:
            User.current_role_id = role_id[0]
        self.manager.current = 'courier'

    def operator(self, *args):
        role_id = []
        if not WithDB().get_smth('get_role_id_with_role_title', ['Оператор'], role_id):
            self.note.universal_note('Произошло обезличивание!', [])
        else:
            User.current_role_id = role_id[0]
        self.manager.current = 'operator'

    def director(self, *args):
        role_id = []
        if not WithDB().get_smth('get_role_id_with_role_title', ['Директор'], role_id):
            self.note.universal_note('Произошло обезличивание!', [])
        else:
            User.current_role_id = role_id[0]
        self.manager.current = 'director'
