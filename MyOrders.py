from kivy.properties import ObjectProperty
from kivy.uix.widget import Widget
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.button import MDTextButton, MDFillRoundFlatButton
from kivymd.uix.screen import MDScreen
from functools import partial
from kivymd.uix.textfield import MDTextField

from DbOperator import DbOperator
from Notification import Notification
from User import User


class MyOrders(MDScreen):
    cont1 = ObjectProperty(None)
    cont2 = ObjectProperty(None)
    titles = []
    dialog = None
    note = Notification(dialog)

    def __init__(self, **kw):
        super().__init__(**kw)

    def on_enter(self, *args):
        self.load_data()

    def fill_any_cont(self, cont, on_press_func, orders_func, add_buttons):
        cont[-1].clear_widgets()
        self.titles.clear()
        customer_id = User.user_id
        orders = orders_func(customer_id)
        for item in orders:
            self.titles.append(item[0])
            cont[-1].add_widget(
                MDTextButton(
                    text='*** ' + str(self.titles[-1]) + ' ***',
                    heigh=80,
                    font_size='30sp',
                    on_press=partial(self.any_ordering, item, on_press_func, add_buttons)
                )
            )

    def any_ordering(self, collection, fun, add_buttons, *args):
        cont = [MDBoxLayout(
            height='410dp',
            orientation='vertical',
            size_hint_y=None
        )]
        widgets = fun(collection, add_buttons)
        for item in widgets:
            cont[0].add_widget(item)
        self.note.note_with_container(cont, "", (.9, .6))

    def processing(self, order_id, *args):
        status_title = 'Оплачен'
        status_description = 'Заказ оплачен клиентом и отмена невозможна.'
        if not DbOperator().alter_orders_status_with_order_id(status_title, order_id, status_description):
            return
        self.load_data()

    def refusing(self, order_id, *args):
        if not DbOperator().refusing_transaction(order_id):
            return
        self.load_data()

    def __widgets_for_any_ordering(self, collection, add_buttons=False):
        txt_field1 = self.__txt_field('Код заказа')
        txt_field1.disabled = True
        txt_field1.text = str(collection[0])
        txt_field2 = self.__txt_field('Дата начала')
        txt_field2.disabled = True
        if collection[1] is not None:
            txt_field2.text = str(collection[1].year) + '-' + str(collection[1].month) + '-' + str(collection[1].day)
        txt_field3 = self.__txt_field('Дата выполнения')
        txt_field3.disabled = True
        if collection[2] is not None:
            txt_field3.text = str(collection[2].year) + '-' + str(collection[2].month) + '-' + str(collection[2].day)
        txt_field4 = self.__txt_field('Статус')
        txt_field4.disabled = True
        txt_field4.text = collection[3]
        txt_field5 = self.__txt_field('Этап')
        txt_field5.disabled = True
        txt_field5.text = collection[4]
        ans = [txt_field1,
               txt_field2,
               txt_field3,
               txt_field4,
               txt_field5,
               Widget()]
        if add_buttons:
            btn1 = self.__button()
            btn1.bind(on_press=partial(self.processing, str(collection[0])))
            btn1.bind(on_release=self.disable_btn)
            btn2 = self.__button()
            btn2.text = 'Отменить заказ'
            btn2.bind(on_press=partial(self.refusing, str(collection[0])))
            if txt_field4.text == 'Оплачен':
                btn2.disabled = True
                btn1.disabled = True
            ans.append(btn1)
            ans.append(Widget())
            ans.append(btn2)
        return ans

    def disable_btn(self, btn, *args):
        btn.disabled = True

    def load_data(self, *args):
        if not DbOperator().try_connection():
            self.note.universal_note('Нет соединеня с одной из БД!', [])
            return
        self.fill_any_cont([self.cont1],
                           self.__widgets_for_any_ordering,
                           DbOperator().get_active_orders_data_for_customer_with_customer_id,
                           True
                           )
        self.fill_any_cont([self.cont2],
                           self.__widgets_for_any_ordering,
                           DbOperator().get_passive_orders_data_for_customer_with_customer_id,
                           False
                           )

    @staticmethod
    def __txt_field(helper_text):
        txt_field = MDTextField()
        txt_field.pos_hint = {'center': .5}
        txt_field.mode = 'rectangle'
        txt_field.size_hint_x = None
        txt_field.size_hint_y = None
        txt_field.height = 40
        txt_field.font_size = 20
        txt_field.width = 350
        txt_field.helper_text_mode = 'persistent'
        txt_field.helper_text = helper_text
        return txt_field

    @staticmethod
    def __button():
        btn = MDFillRoundFlatButton()
        btn.pos_hint = {'center': .5}
        btn.font_size = 15
        btn.md_bg_color = [40 / 255, 40 / 255, 180 / 255, 100 / 255]
        btn.text_color = [1, 1, 1, 1]
        btn.size_hint_x = None
        btn.text = 'Оплатить заказ'
        return btn
