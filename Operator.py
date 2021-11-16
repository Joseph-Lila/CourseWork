from kivy.properties import ObjectProperty
from kivy.uix.togglebutton import ToggleButton
from kivy.uix.widget import Widget
from kivymd.uix.screen import MDScreen

import User
from DbOperator import DbOperator
from Notification import Notification


class Operator(MDScreen):
    cont1 = ObjectProperty(None)
    cont2 = ObjectProperty(None)
    titles = []
    dialog = None
    note = Notification(dialog)

    def __init__(self, **kw):
        super().__init__(**kw)

    def on_enter(self, *args):
        self.load_data()

    def fill_any_cont(self, cont, get_func, group_number):
        cont[-1].clear_widgets()
        self.titles.clear()
        items_to_show = get_func()
        if len(items_to_show) == 0:
            return
        cont[-1].add_widget(Widget())
        for i in range(len(items_to_show)):
            self.titles.append(items_to_show[i])
            cont[-1].add_widget(ToggleButton(text=str(self.titles[-1]),
                                             size_hint_y=None,
                                             height='48dp',
                                             group=group_number
                                             )
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
        stage_id = DbOperator().get_stage_id_with_stage_title('Выполняется')
        if stage_id == -1:
            self.note.universal_note('Операция была прервана!', [])
            return
        if not DbOperator().add_courier_id_and_operator_id_into_order_with_order_id(courier_id,
                                                                                    User.User.user_id,
                                                                                    stage_id,
                                                                                    order_id
                                                                                    ):
            self.note.universal_note('Операция была прервана!', [])
            return
        if not DbOperator().change_courier_status(courier_id,
                                                  DbOperator().get_status_id_with_status_title('Занят')
                                                  ):
            self.note.universal_note('Операция прервана!', [])
            return
        self.note.universal_note('Заказ был передан курьеру!', [])

    def load_data(self, *args):
        self.fill_any_cont([self.cont1], DbOperator().get_free_couriers, 'g1')
        self.fill_any_cont([self.cont2], DbOperator().get_paid_orders, 'g2')

