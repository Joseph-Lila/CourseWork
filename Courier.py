from kivy.properties import ObjectProperty
from kivy.uix.image import Image
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.screen import MDScreen

from DbOperator import DbOperator
from Notification import Notification
from User import User


class Courier(MDScreen):
    label = ObjectProperty(None)
    btn1 = ObjectProperty(None)
    btn2 = ObjectProperty(None)
    check = False
    dialog = None
    note = Notification(dialog)

    def __init__(self, **kw):
        super().__init__(**kw)

    def on_enter(self, *args):
        self.load_data()

    def load_data(self):
        if not DbOperator().try_connection():
            self.note.universal_note('Нет соединеня с одной из БД!', [])
            return
        if DbOperator().when_shall_i_be_free(User.user_id):
            self.check = False
            self.label.text = 'Заказов нет'
            self.btn1.disabled = True
            self.btn2.disabled = True
            return
        else:
            self.check = True
            self.label.text = 'Появился новый заказ!'
            self.btn1.disabled = False
            self.btn2.disabled = False

    def completed(self):
        if not DbOperator().order_completed_transaction(User.user_id):
            self.note.universal_note('Операция прервана!', [])
            return
        self.note.universal_note('Изменения были зафиксированы!', [])
        self.load_data()

    def info(self):
        cont = MDBoxLayout(
                height='700dp',
                orientation='vertical',
                size_hint_y=None)
        im = Image(source='pictures/map2.jpg')
        cont.add_widget(im)
        self.note.note_with_container([cont], "", (700 / 1920, 500, 1080))
