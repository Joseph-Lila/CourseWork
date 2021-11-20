from kivy.properties import ObjectProperty
from kivymd.uix.screen import MDScreen
import matplotlib as mpl
import matplotlib.pyplot as plt
from DbOperator import DbOperator
from kivy.uix.image import Image


class Reports(MDScreen):
    services_pie = ObjectProperty(None)
    months_pie = ObjectProperty(None)
    cities_pie = ObjectProperty(None)

    def __init__(self, **kw):
        super().__init__(**kw)

    def on_enter(self, *args):
        self.load_data()

    def go_back(self, *args):
        self.manager.current = 'director'

    def fill_services_pie(self):
        self.__get_pie(DbOperator().get_services_titles_and_total_costs, "Доходы по услугам (%)")
        self.services_pie.add_widget(Image(source='pictures/pieДоходы по услугам (%).png'))

    def fill_months_pie(self):
        self.__get_pie(DbOperator().get_months_quantity_orders, "Услуги по месяцам  (%)")
        self.months_pie.add_widget(Image(source='pictures/pieУслуги по месяцам  (%).png'))

    def fill_cities_pie(self):
        self.__get_pie(DbOperator().get_cities_quantity_orders, "Услуги по городам  (%)")
        self.cities_pie.add_widget(Image(source='pictures/pieУслуги по городам  (%).png'))

    @staticmethod
    def __get_pie(func, title):
        data_collection = func()
        data_names = [item[0] for item in data_collection]
        data_values = [item[1] for item in data_collection]
        dpi = 80
        fig = plt.figure(dpi=dpi, figsize=(512 / dpi, 384 / dpi))
        mpl.rcParams.update({'font.size': 9})
        plt.title(title)
        xs = range(len(data_names))
        plt.pie(
            data_values, autopct='%.1f', radius=1.2,
            explode=[0.15] + [0 for item in range(len(data_names) - 1)])
        plt.legend(
            bbox_to_anchor=(-0.16, 0.45, 0.25, 0.25),
            loc='lower left', labels=data_names)
        fig.savefig(f'pictures/pie{title}.png')

    def load_data(self):
        if not DbOperator().try_connection():
            self.note.universal_note('Нет соединеня с одной из БД!', [])
            return
        self.fill_cities_pie()
        self.fill_services_pie()
        self.fill_months_pie()
