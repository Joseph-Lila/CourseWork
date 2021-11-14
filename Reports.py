from kivy.properties import ObjectProperty
from kivy_garden.graph import MeshLinePlot
from kivymd.uix.screen import MDScreen

from kivy.uix.floatlayout import FloatLayout
import matplotlib.dates as mdates
import matplotlib
from matplotlib import pylab
from WithDB import WithDB


class Reports(MDScreen):
    statistic = ObjectProperty(None)
    volume_per_month = ObjectProperty(None)

    def __init__(self, **kw):
        super().__init__(**kw)

    def on_enter(self, *args):
        self.load_data()

    def fill_statistic(self):
        pass

    def fill_volume_per_month(self):
        pass

    def load_data(self):
        self.fill_volume_per_month()
        self.fill_statistic()
