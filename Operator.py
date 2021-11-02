from random import randrange

from kivy.properties import ObjectProperty
from kivy.uix.togglebutton import ToggleButton
from kivy.uix.widget import Widget
from kivymd.uix.label import MDLabel
from kivymd.uix.screen import MDScreen

import User
from Notification import Notification
from WithDB import WithDB


class Operator(MDScreen):
    cont1 = ObjectProperty(None)
    cont2 = ObjectProperty(None)
    titles = []
    dialog = None
    note = Notification(dialog)

    def __init__(self, **kw):
        super().__init__(**kw)
        self.fill_first_cont()
        self.fill_second_cont()

    def fill_first_cont(self):
        self.cont1.clear_widgets()
        self.titles.clear()
        db_pointer = WithDB()
        couriers = []
        if not db_pointer.get_smth('get_free_couriers', [], couriers):
            return None
        if len(couriers) == 0:
            return None
        self.cont1.add_widget(Widget())
        for i in range(len(couriers)):
            self.titles.append(couriers[i][0])
            self.cont1.add_widget(ToggleButton(text=str(self.titles[-1]),
                                               size_hint_y=None,
                                               height='48dp',
                                               group='g1')
                                  )

    def link(self):
        order_id = 0
        courier_id = 0
        for i in self.cont1.children:
            if isinstance(i, ToggleButton) and i.state == 'down':
                courier_id = i.text
        for i in self.cont2.children:
            if isinstance(i, ToggleButton) and i.state == 'down':
                order_id = i.text
        db_pointer = WithDB()
        stage_id = []
        if not db_pointer.get_smth('get_stage_id_with_stage_title', ['Выполняется'], stage_id):
            self.note.universal_note('Операция была прервана!', [])
            return None
        stage_id = stage_id[0][0]
        if not db_pointer.insert_delete_alter_smth('add_courier_id_and_operator_id_into_order_with_order_id',
                                                   [str(courier_id), str(User.User.user_id), str(stage_id), str(order_id)]):
            self.note.universal_note('Операция была прервана!', [])
            return None
        self.note.universal_note('Заказ был передан курьеру!', [])

    def fill_second_cont(self):
        self.cont2.clear_widgets()
        self.titles.clear()
        db_pointer = WithDB()
        orders = []
        if not db_pointer.get_smth('get_paid_orders', [], orders):
            return None
        if len(orders) == 0:
            return None
        self.cont2.add_widget(Widget())
        for i in range(len(orders)):
            self.titles.append(orders[i][0])
            self.cont2.add_widget(ToggleButton(text=str(self.titles[-1]),
                                               size_hint_y=None,
                                               height='48dp',
                                               group='g2'
                                               )
                                  )

    def load_data(self, *args):
        self.fill_first_cont()
        self.fill_second_cont()

