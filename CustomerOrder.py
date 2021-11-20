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

from DbOperator import DbOperator
from Notification import Notification
from kivy.uix.button import Button

from collections import namedtuple
from RightCheckbox import RightCheckbox


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
        cont = [MDBoxLayout(
            height='500dp',
            orientation='vertical',
            size_hint_y=None
        )]
        widgets = self.__widgets_for_ordering(title)
        for i in range(len(widgets)):
            cont[0].add_widget(widgets[i])
        self.note.note_with_container(cont, "Оформление заказа", (.9, .6))

    def processing(self, order_creator, *args):
        if not DbOperator().try_connection():
            self.note.universal_note('Нет соединеня с одной из БД!', [])
            return
        for value in order_creator:
            if hasattr(value, 'text'):
                if value.text == '':
                    self.note.universal_note('Заполните все поля!', [])
                    return
            else:
                if value == '':
                    self.note.universal_note('Заполните все поля!', [])
                    return
        RightCheckbox.my_collection.append(order_creator)
        # self.note.universal_note('Услуга успешно добавлена!', [])


    @staticmethod
    def __is_number(value):
        try:
            float(value)
            return True
        except ValueError:
            return False

    def __calculator(self, collection, *args):
        costs = DbOperator().get_services_costs_with_title(collection[0])
        if len(costs) == 0:
            self.note.universal_note('Проблемы с БД!', [])
            return
        cost_weight = float(costs[0])
        cost_radius = float(costs[1])
        if self.__is_number(collection[1].text) and self.__is_number(collection[2].text):
            collection[3].text = str(float(
                collection[1].text) * cost_weight + float(collection[2].text) * cost_radius)
        else:
            self.note.universal_note('Вес и расстояние - числа!', [collection[1]])

    def __widgets_for_ordering(self, title):
        txt_field1 = self.__txt_field(title)
        txt_field1.disabled = True
        departure_field = self.__txt_field('Адрес отправления')
        destination_field = self.__txt_field('Адрес назначения')
        weight_field = self.__txt_field('Вес (кг)')
        weight_field.text = '0'
        radius_field = self.__txt_field('Расстояние (км)')
        radius_field.text = '0'
        total_cost_field = self.__txt_field('Итоговая стоимость')
        total_cost_field.disabled = True
        weight_field.bind(on_text_validate=partial(self.__calculator, [title, weight_field, radius_field, total_cost_field]))
        radius_field.bind(on_text_validate=partial(self.__calculator, [title, weight_field, radius_field, total_cost_field]))
        #---------------------------
        label1 = self.__label('Город отправления')
        label2 = self.__label('Город назначения')
        self.titles.clear()
        sp_cities = DbOperator().get_city_titles()
        sp1 = 'pass'
        sp2 = 'pass'
        if len(sp_cities) == 0:
            sp1 = self.__spinner(['Пусто'])
            sp2 = self.__spinner(['Пусто'])
        else:
            for item in sp_cities:
                self.titles.append(item)
            sp1 = self.__spinner(self.titles)
            sp2 = self.__spinner(self.titles)
        grid1 = GridLayout(cols=2, rows=None)
        grid2 = GridLayout(cols=2, rows=None)
        grid1.add_widget(label1)
        grid1.add_widget(sp1)
        grid2.add_widget(label2)
        grid2.add_widget(sp2)
        btn1 = self.__button()
        OrderCreator = namedtuple('OrderCreator',
                                  ['begin_city', 'departure', 'end_city',
                                   'destination', 'weight', 'radius',
                                   'total_cost', 'title']
                                  )
        order_creator = OrderCreator(begin_city=sp1, departure=departure_field,
                                     end_city=sp2, destination=destination_field,
                                     weight=weight_field, radius=radius_field,
                                     total_cost=total_cost_field, title=title
                                     )
        btn1.bind(on_press=partial(self.processing, order_creator))
        return [txt_field1, grid1, departure_field, grid2, destination_field,
                weight_field, radius_field, total_cost_field, Widget(), btn1]

    @staticmethod
    def __button():
        btn = MDFillRoundFlatButton()
        btn.pos_hint = {'center': .5}
        btn.font_size = 15
        btn.md_bg_color = [40 / 255, 40 / 255, 180 / 255, 100 / 255]
        btn.text_color = [1, 1, 1, 1]
        btn.size_hint_x = None
        btn.text = 'Подтвердить заказ и добавить в корзину.'
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
        txt_field.write_tab = False
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
        services = DbOperator().get_service_titles()
        if len(services) == 0:
            self.cont.add_widget(MDLabel(text='Список пуст.'))
            return
        for item in services:
            self.titles.append(item)
            self.cont.add_widget(MDTextButton(text='- ' + item,
                                              heigh=80,
                                              font_size='30sp',
                                              on_press=partial(self.ordering, item)
                                              )
                                        )
