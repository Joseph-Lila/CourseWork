import datetime
from kivy.properties import ObjectProperty
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.spinner import Spinner
from kivy.uix.widget import Widget
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.button import MDTextButton, MDFillRoundFlatButton
from kivymd.uix.label import MDLabel
from kivymd.uix.screen import MDScreen
from functools import partial
from kivymd.uix.textfield import MDTextField
from Notification import Notification
from User import User
from WithDB import WithDB
from kivy.uix.button import Button


class CustomerOrder(MDScreen):
    cont = ObjectProperty(None)
    titles = []
    dialog = None
    note = Notification(dialog)
    container = BoxLayout()

    def __init__(self, **kw):
        super().__init__(**kw)
        self.fill_services()
        self.container.add_widget(Button(text='Hello'))

    def ordering(self, title, *args):
        cont = []
        cont.append(MDBoxLayout(
            height='500dp',
            orientation='vertical',
            size_hint_y=None
        )
        )
        widgets = self.__widgets_for_ordering(title)
        for i in range(len(widgets)):
            cont[0].add_widget(widgets[i])
        self.note.note_with_container(cont)

    def processing(self, collection, *args):
        for i in range(len(collection) - 1):
            if collection[i].text == '':
                self.note.universal_note('Заполните все поля!', [])
                return None
        now = datetime.datetime.date(datetime.datetime.today())
        customer_id = []
        db_pointer = WithDB()
        if not db_pointer.get_smth('get_customer_id_with_user_id', [User.user_id], customer_id):
            self.note.universal_note('Проблемы с БД!', [])
            return None
        else:
            customer_id = customer_id[0][0]
        stage_id = []
        if not db_pointer.get_smth('get_stage_id_with_stage_title', ['На рассмотрении'], stage_id):
            self.note.universal_note('Проблемы с БД!', [])
            return None
        else:
            stage_id = stage_id[0][0]
        status_id = []
        if not db_pointer.get_smth('get_status_id_with_status_title', ['Не оплачен'], status_id):
            self.note.universal_note('Проблемы с БД!', [])
            return None
        else:
            status_id = status_id[0][0]
        if not db_pointer.insert_delete_alter_smth('add_order', [now, customer_id, stage_id, status_id]):
            self.note.universal_note('Заказ не был создан!', [])
            return None
        print(status_id)
        orders_id = []
        if not db_pointer.get_smth('get_last_orders_id', [now, customer_id, stage_id, status_id], orders_id):
            self.note.universal_note('Проблемы с БД!', [])
            return None
        else:
            print(orders_id)
            orders_id = orders_id[0][0]
        service_id = []
        if not db_pointer.get_smth('get_service_with_title', [collection[-1]], service_id):
            self.note.universal_note('Проблемы с БД!', [])
            return None
        else:
            service_id = service_id[0][0]
        if not db_pointer.insert_delete_alter_smth('insert_my_orders_service', [service_id, orders_id, collection[4].text,
                                                                                collection[5].text, collection[3].text,
                                                                                collection[1].text, collection[6].text]):
            self.note.universal_note('Услуга заказа не была добавлена!', [])
            return None
        orders_service_id = []
        if not db_pointer.get_smth('get_my_orders_service_id', [service_id, orders_id, collection[4].text, collection[5].text,
                  collection[3].text, collection[1].text, collection[6].text], orders_service_id):
            self.note.universal_note('Проблемы с БД!', [])
            return None
        orders_service_id = orders_service_id[0][0]
        begin_city_id = []
        end_city_id = []
        if not db_pointer.get_smth('get_city_id_with_city_title',
                                   [collection[0].text], begin_city_id):
            self.note.universal_note('Проблемы с БД!', [])
            return None
        if not db_pointer.get_smth('get_city_id_with_city_title',
                                   [collection[2].text], end_city_id):
            self.note.universal_note('Проблемы с БД!', [])
            return None
        begin_city_id = begin_city_id[0][0]
        end_city_id = end_city_id[0][0]
        if not db_pointer.insert_delete_alter_smth('insert_order_services_begin_city',
                                                   [begin_city_id, orders_service_id]):
            self.note.universal_note('Начальный город услуги заказа не был добавлен!', [])
            return None
        if not db_pointer.insert_delete_alter_smth('insert_order_services_end_city',
                                                   [end_city_id, orders_service_id]):
            self.note.universal_note('Конечный город услуги заказа не был добавлен!', [])
            return None
        self.note.universal_note('Операция прошла успешно!', [])

    @staticmethod
    def __is_number(value):
        try:
            float(value)
            return True
        except ValueError:
            return False

    def __calculator(self, collection, *args):
        db_pointer = WithDB()
        costs = []
        cost_weight = 0
        cost_radius = 0
        if not db_pointer.get_smth('get_services_costs_with_title', [collection[0]], costs):
            self.note.universal_note('Проблемы с БД!', [])
            return None
        else:
            cost_weight = float(costs[0][0])
            cost_radius = float(costs[0][1])
            if self.__is_number(collection[1].text) and self.__is_number(collection[2].text):
                collection[3].text = str(float(
                    collection[1].text) * cost_weight + float(collection[2].text) * cost_radius)
            else:
                self.note.universal_note('Вес и расстояние - числа!', [collection[1]])

    def __widgets_for_ordering(self, title):
        txt_field1 = self.__txt_field(title)
        txt_field1.disabled = True
        txt_field2 = self.__txt_field('Адрес отправления')
        txt_field3 = self.__txt_field('Адрес назначения')
        txt_field4 = self.__txt_field('Вес (кг)')
        txt_field5 = self.__txt_field('Расстояние (км)')
        txt_field5.text = '23.2'
        txt_field5.disabled = True
        txt_field6 = self.__txt_field('Итоговая стоимость')
        txt_field6.disabled = True
        txt_field4.bind(on_text_validate=partial(self.__calculator, [title, txt_field4, txt_field5, txt_field6]))
        txt_field5.bind(on_text_validate=partial(self.__calculator, [title, txt_field4, txt_field5, txt_field6]))
        #---------------------------
        label1 = self.__label('Город отправления')
        label2 = self.__label('Город назначения')
        self.titles.clear()
        db_pointer = WithDB()
        sp_cities = []
        sp1 = 'pass'
        sp2 = 'pass'
        if not db_pointer.get_smth('get_city_titles', [], sp_cities):
            sp1 = self.__spinner(['Пусто'])
            sp2 = self.__spinner(['Пусто'])
        else:
            for i in range(len(sp_cities)):
                self.titles.append(sp_cities[i][0])
            sp1 = self.__spinner(self.titles)
            sp2 = self.__spinner(self.titles)
        grid1 = GridLayout(cols=2,
                           rows=None)
        grid2 = GridLayout(cols=2,
                           rows=None)
        grid1.add_widget(label1)
        grid1.add_widget(sp1)
        grid2.add_widget(label2)
        grid2.add_widget(sp2)
        btn1 = self.__button()
        btn1.bind(on_press=partial(self.processing, [sp1,
                                                     txt_field2,
                                                     sp2,
                                                     txt_field3,
                                                     txt_field4,
                                                     txt_field5,
                                                     txt_field6,
                                                     title
                                                     ]
                                   )
                  )
        return [txt_field1,
                grid1,
                txt_field2,
                grid2,
                txt_field3,
                txt_field4,
                txt_field5,
                txt_field6,
                Widget(),
                btn1
                ]

    @staticmethod
    def __button():
        btn = MDFillRoundFlatButton()
        btn.pos_hint = {'center': .5}
        btn.font_size = 15
        btn.md_bg_color = [40 / 255, 40 / 255, 180 / 255, 100 / 255]
        btn.text_color = [1, 1, 1, 1]
        btn.size_hint_x = None
        btn.text = 'Подтвердить заказ'
        return btn

    @staticmethod
    def __spinner(collection):
        sp = Spinner()
        sp.text = collection[0]
        sp.values = tuple(collection)
        sp.size_hint = (None, None)
        sp.size = (165, 40)
        sp.pos_hint = {'center': .5}
        return sp

    @staticmethod
    def __label(text):
        label = MDLabel(text=text)
        label.pos_hint = {'center': .5}
        label.size_hint_x = None
        label.size_hint_y = None
        label.height = 40
        label.width = 185
        label.color = [249 / 255, 166 / 255, 2 / 255, 255 / 255]
        return label

    @staticmethod
    def __txt_field(hint_text):
        txt_field = MDTextField()
        txt_field.pos_hint = {'center': .5}
        txt_field.color_mode = 'primary'
        txt_field.mode = 'rectangle'
        txt_field.size_hint_x = None
        txt_field.size_hint_y = None
        txt_field.height = 40
        txt_field.font_size = 20
        txt_field.width = 350
        txt_field.hint_text = hint_text
        return txt_field

    def fill_services(self, *args):
        self.cont.clear_widgets()
        self.titles.clear()
        db_pointer = WithDB()
        services = []
        if not db_pointer.get_smth('get_service_titles', [], services):
            self.cont.add_widget(MDLabel(text='Список пуст.'))
        else:
            for i in range(len(services)):
                self.titles.append(services[i][0])
                self.cont.add_widget(MDTextButton(text='- ' + services[i][0],
                                                  heigh=80,
                                                  font_size='30sp',
                                                  on_press=partial(self.ordering, services[i][0])
                                                  )
                                            )
