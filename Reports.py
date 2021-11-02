from kivy.properties import ObjectProperty
from kivymd.uix.screen import MDScreen
import matplotlib.dates as mdates
import matplotlib
from matplotlib import pylab
from WithDB import WithDB


class Reports(MDScreen):
    statistic = ObjectProperty(None)
    volume_per_month = ObjectProperty(None)

    def __init__(self, **kw):
        super().__init__(**kw)
        self.fill_volume_per_month()
        self.fill_statistic()

    def fill_statistic(self):
        self.__profit_per_month()
        self.__services_diagramm()
        self.__customers_cities_giagramm()

    def fill_volume_per_month(self):
        pass

    def __profit_per_month(self):
        db_pointer = WithDB()
        data = []
        if not db_pointer.get_smth('get_sum_profit_for_each_month', [], data):
            return None
        if len(data) == 0:
            return None
        dates = []
        y = []
        for i in range(len(data)):
            dates.append(data[i][0])
            y.append(data[i][1])
        xdata_float = matplotlib.dates.date2num(dates)
        axes = pylab.subplot(1, 1, 1)
        axes.xaxis.set_major_formatter(matplotlib.dates.DateFormatter('%Y'))
        pylab.plot_date(xdata_float, y, fmt='b-')
        pylab.grid()
        pylab.savefig('pictures/profit_per_month.png')

    def __services_diagramm(self):
        db_pointer = WithDB()
        data = []
        if not db_pointer.get_smth('get_quantity_of_each_services_item', [], data):
            return None
        if len(data) == 0:
            return None
        print(data)

    def __customers_cities_giagramm(self):
        pass

    def load_data(self):
        self.fill_volume_per_month()
        self.fill_statistic()
