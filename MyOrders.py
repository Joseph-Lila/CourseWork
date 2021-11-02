import datetime

from kivy.properties import ObjectProperty
from kivy.uix.widget import Widget
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.button import MDTextButton, MDFillRoundFlatButton
from kivymd.uix.label import MDLabel
from kivymd.uix.screen import MDScreen
from functools import partial
from random import randrange
from kivymd.uix.textfield import MDTextField
from Notification import Notification
from User import User
from WithDB import WithDB


class MyOrders(MDScreen):
    cont1 = ObjectProperty(None)
    cont2 = ObjectProperty(None)
    titles = []
    dialog = None
    note = Notification(dialog)

    def __init__(self, **kw):
        super().__init__(**kw)
        self.fill_first_cont()
        self.fill_second_cont()

    def fill_second_cont(self):
        self.cont2.clear_widgets()
        self.titles.clear()
        db_pointer = WithDB()
        customer_id = []
        if not db_pointer.get_smth('get_customer_id_with_user_id', [User.user_id], customer_id):
            return None
        if len(customer_id) == 0:
            return None
        customer_id = customer_id[0][0]
        db_pointer = WithDB()
        orders = []
        if not db_pointer.get_smth('get_passive_orders_data_for_customer_with_customer_id', [customer_id], orders):
            self.cont2.add_widget(MDLabel(text='Список пуст.'))
        else:
            for i in range(len(orders)):
                self.titles.append(orders[i][0])

                self.cont2.add_widget(MDTextButton(text='*** ' + str(self.titles[-1]) + ' ***',
                                                   heigh=80,
                                                   custom_color=[randrange(256) / 255, randrange(256) / 255,
                                                                 randrange(256) / 255, 255 / 255],
                                                   font_size='30sp',
                                                   on_press=partial(self.ordering_second, orders[i])
                                                   )
                                      )

    def fill_first_cont(self):
        self.cont1.clear_widgets()
        self.titles.clear()
        db_pointer = WithDB()
        customer_id = []
        if not db_pointer.get_smth('get_customer_id_with_user_id', [User.user_id], customer_id):
            return None
        if len(customer_id) == 0:
            return None
        customer_id = customer_id[0][0]
        orders = []
        if not db_pointer.get_smth('get_active_orders_data_for_customer_with_customer_id', [customer_id], orders):
            self.cont1.add_widget(MDLabel(text='Список пуст.'))
        else:
            for i in range(len(orders)):
                self.titles.append(orders[i][0])

                self.cont1.add_widget(MDTextButton(text='*** ' + str(self.titles[-1]) + ' ***',
                                                   heigh=80,
                                                   custom_color=[randrange(256) / 255, randrange(256) / 255,
                                                                 randrange(256) / 255, 255 / 255],
                                                   font_size='30sp',
                                                   on_press=partial(self.ordering, orders[i])
                                                   )
                                      )

    def ordering(self, collection, *args):
        cont = []
        cont.append(MDBoxLayout(
            height='410dp',
            orientation='vertical',
            size_hint_y=None
        )
        )
        widgets = self.__widgets_for_ordering(collection)
        for i in range(len(widgets)):
            cont[0].add_widget(widgets[i])
        self.note.note_with_container(cont)

    def ordering_second(self, collection, *args):
        cont = []
        cont.append(MDBoxLayout(
            height='410dp',
            orientation='vertical',
            size_hint_y=None
        )
        )
        widgets = self.__widgets_for_ordering_second(collection)
        for i in range(len(widgets)):
            cont[0].add_widget(widgets[i])
        self.note.note_with_container(cont)

    def processing(self, order_id, *args):
        db_pointer = WithDB()
        status_id = []
        if not db_pointer.get_smth('get_status_id_with_status_title', ['Оплачен'], status_id):
            return None
        else:
            status_id = status_id[0][0]
        if not db_pointer.insert_delete_alter_smth('alter_orders_status_id_with_order_id',
                                                   [status_id, order_id]):
            return None
        self.fill_first_cont()
        self.fill_second_cont()

    def refusing(self, order_id, *args):
        db_pointer = WithDB()
        stage_id = []
        now = datetime.datetime.date(datetime.datetime.today())
        if not db_pointer.get_smth('get_stage_id_with_stage_title', ['Отменен'], stage_id):
            return None
        else:
            stage_id = stage_id[0][0]
        if not db_pointer.insert_delete_alter_smth('add_orders_executions_and_stage_id_with_order_id',
                                                   [now, stage_id, order_id]):
            return None
        self.fill_first_cont()
        self.fill_second_cont()

    def __widgets_for_ordering(self, collection):
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
        btn1 = self.__button()
        btn1.bind(on_press=partial(self.processing, str(collection[0])))
        btn2 = self.__button()
        btn2.text = 'Отменить заказ'
        btn2.bind(on_press=partial(self.refusing, str(collection[0])))
        if txt_field4.text == 'Оплачен':
            btn2.disabled = True

        return [txt_field1,
                txt_field2,
                txt_field3,
                txt_field4,
                txt_field5,
                Widget(),
                btn1,
                Widget(),
                btn2]

    def __widgets_for_ordering_second(self, collection):
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
        return [txt_field1,
                txt_field2,
                txt_field3,
                txt_field4,
                txt_field5,
                Widget()]

    def load_data(self, *args):
        self.fill_first_cont()
        self.fill_second_cont()

    @staticmethod
    def __txt_field(text_hint):
        txt_field = MDTextField()
        txt_field.pos_hint = {'center': .5}
        txt_field.color_mode = 'primary'
        txt_field.mode = 'rectangle'
        txt_field.size_hint_x = None
        txt_field.size_hint_y = None
        txt_field.height = 40
        txt_field.font_size = 20
        txt_field.width = 350
        txt_field.text_hint = text_hint
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
