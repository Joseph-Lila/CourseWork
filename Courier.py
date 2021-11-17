from kivy.properties import ObjectProperty
from kivy.uix.image import Image
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
        if not DbOperator().when_shall_i_be_free(User.user_id):
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
        im = Image(source='pictures/map.jpg')
        im.allow_stretch = True
        im.size_hint_x = None
        im.size_hint_y = None
        im.height = 800
        im.width = 1400
        self.note.note_with_container([im], "")
