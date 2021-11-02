from datetime import datetime

from kivy.properties import ObjectProperty
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.image import Image
from kivymd.uix.screen import MDScreen

from Notification import Notification
from User import User
from WithDB import WithDB


class Courier(MDScreen):
    label = ObjectProperty(None)
    btn1 = ObjectProperty(None)
    btn2 = ObjectProperty(None)
    check = False
    dialog = None
    note = Notification(dialog)

    def __init__(self, **kw):
        super().__init__(**kw)
        self.load_data()

    def load_data(self):
        ans = []
        db_pointer = WithDB()
        if not db_pointer.get_smth('get_order_with_courier_id', [User.user_id], ans):
            self.check = False
            self.label.text = 'Заказов нет'
            self.btn1.disabled = True
            self.btn2.disabled = True
            return None
        elif len(ans) == 0:
            self.check = False
            self.label.text = 'Заказов нет'
            self.btn1.disabled = True
            self.btn2.disabled = True
            return None
        else:
            self.check = True
            ans = ans[0][0]
            self.label.text = 'Заказ № ' + str(ans)
            self.btn1.disabled = False
            self.btn2.disabled = False

    def completed(self):
        ans = []
        db_pointer = WithDB()
        if not db_pointer.get_smth('get_order_with_courier_id', [User.user_id], ans):
            self.note.universal_note('Ошибка подключения к базе данных!', [])
            return None
        if len(ans) == 0:
            self.note.universal_note('Неизвестная ошибка!', [])
            return None
        ans = ans[0][0]
        now = datetime.date(datetime.today())
        stage_id = []
        if not db_pointer.get_smth('get_stage_id_with_stage_title', ['Выполнен'], stage_id):
            return None
        else:
            stage_id = stage_id[0][0]
        if not db_pointer.insert_delete_alter_smth('add_orders_executions_and_stage_id_with_order_id',
                                                   [now, stage_id, ans]):
            self.note.universal_note('Операция была прервана!', [])
            return None
        self.note.universal_note('Изменения были зафиксированы!', [])
        self.load_data()

    def info(self):
        im = Image(source='pictures/map.jpg')
        im.allow_stretch = True
        im.size_hint_x = None
        im.size_hint_y = None
        im.height = 800
        im.width = 1400
        self.note.note_with_container([im])
