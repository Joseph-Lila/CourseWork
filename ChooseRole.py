from kivy.app import App
from kivy.uix.anchorlayout import AnchorLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.widget import Widget
from kivymd.uix.button import MDFillRoundFlatButton, MDIconButton
from kivymd.uix.card import MDCard
from kivymd.uix.screen import MDScreen
from functools import partial
from DbOperator import DbOperator
from Notification import Notification
from User import User


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
        self.__add_buttons()

    def __add_buttons(self):
        main_container = self.__main_container()
        main_container.add_widget(self.__icons())
        main_container.add_widget(Widget())
        self.buttons["Клиент"] = self.__any_button('Клиент', 'customer')
        self.buttons['Курьер'] = self.__any_button('Курьер', 'courier')
        self.buttons['Оператор'] = self.__any_button('Оператор', 'operator')
        self.buttons['Директор'] = self.__any_button('Директор', 'director')
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

    def __any_button(self, title_rus, title_en):
        button = MDFillRoundFlatButton()
        button.disabled = True
        button.pos_hint = {"center_x": .5}
        button.font_size = 15
        button.md_bg_color = [10 / 255, 10 / 255, 140 / 255, 100 / 255]
        button.text_color = [1, 1, 1, 1]
        button.text = title_rus
        button.bind(on_press=partial(self.__role, title_rus, title_en))
        return button

    def __role(self, title_rus, title_en, *args):
        role_id = DbOperator().get_role_id_with_role_title(title_rus)
        if role_id == -1:
            self.note.universal_note('Произошло обезличивание!', [])
        else:
            User.current_role_id = role_id
        self.manager.current = title_en
