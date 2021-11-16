from datetime import datetime

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
        ans = DbOperator().get_order_id_with_courier_id(User.user_id)
        if ans == -1:
            self.check = False
            self.label.text = 'Заказов нет'
            self.btn1.disabled = True
            self.btn2.disabled = True
            return
        else:
            self.check = True
            self.label.text = 'Заказ № ' + str(ans)
            self.btn1.disabled = False
            self.btn2.disabled = False

    def completed(self):
        ans = DbOperator().get_order_id_with_courier_id(User.user_id)
        if ans == -1:
            self.note.universal_note('Ошибка подключения к базе данных!', [])
            return
        now = datetime.today().strftime("%Y-%d-%m %H:%M:%S")
        stage_id = DbOperator().get_stage_id_with_stage_title('Выполнен')
        if stage_id == -1:
            return
        else:
            if not DbOperator().add_orders_executions_and_stage_id_with_order_id(now, stage_id, ans):
                self.note.universal_note('Операция была прервана!', [])
                return
        if not DbOperator().change_courier_status(User.user_id,
                                                  DbOperator().get_status_id_with_status_title('Свободен')
                                                  ):
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
