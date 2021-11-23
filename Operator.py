from kivy.properties import ObjectProperty
from kivy.uix.togglebutton import ToggleButton
from kivy.uix.widget import Widget
from kivymd.uix.screen import MDScreen
from DbOperator import concat_n_words, split_n_words
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
            self.titles.append(concat_n_words(items_to_show[i]))
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
                courier_id = split_n_words(i.text)
        for i in self.cont2.children:
            if isinstance(i, ToggleButton) and i.state == 'down':
                order_id = split_n_words(i.text)
        if not DbOperator().linking_transaction(User.User.user_id,
                                                courier_id,
                                                order_id):
            self.note.universal_note('Операция прервана!', [])
            return
        self.note.universal_note('Заказ был передан курьеру!', [])

    def load_data(self, *args):
        if not DbOperator().try_connection():
            self.note.universal_note('Нет соединеня с одной из БД!', [])
            return
        self.fill_any_cont([self.cont1], DbOperator().get_free_couriers, 'g1')
        self.fill_any_cont([self.cont2], DbOperator().get_paid_orders, 'g2')

