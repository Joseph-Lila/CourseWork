from kivy.config import Config

Config.set('kivy', 'keyboard_mode', 'systemanddock')
Config.set('graphics', 'resizable', False)
Config.set("graphics", "width", 480)
Config.set("graphics", "height", 850)

from kivymd.app import MDApp
from kivy.uix.screenmanager import ScreenManager, FallOutTransition
from kivy.lang import Builder

from CustomerOrder import CustomerOrder
from Director import *
from Customer import *
from ChooseRole import ChooseRole
from HandBooks import HandBooks
from LogIn import LogIn
from Reports import Reports
from SignUp import *
from GetPassword import *
from Operator import Operator
from Courier import Courier
from MyOrders import MyOrders
from CustomerOrderBasket import CustomerOrderBasket


import MSSql,MongoDB, DB_Recorder


Builder.load_file('kv-files/My.kv')
Builder.load_file('kv-files/LogIn.kv')
Builder.load_file('kv-files/SignUp.kv')
Builder.load_file('kv-files/GetPassword.kv')
Builder.load_file('kv-files/Customer.kv')
Builder.load_file('kv-files/Director.kv')
Builder.load_file('kv-files/Operator.kv')
Builder.load_file('kv-files/Courier.kv')
Builder.load_file('kv-files/HandBooks.kv')
Builder.load_file('kv-files/CustomerOrder.kv')
Builder.load_file('kv-files/Reports.kv')
Builder.load_file('kv-files/MyOrders.kv')
Builder.load_file('kv-files/CustomerOrderBasket.kv')


class Myapp(MDApp):
    title = 'CourseWork'

    def build(self):
        sm = ScreenManager(transition=FallOutTransition())
        sm.add_widget(LogIn(name='login'))
        sm.add_widget(SignUp(name='sign_up'))
        sm.add_widget(GetPassword(name='get_password'))
        sm.add_widget(ChooseRole(name='choose_role'))
        sm.add_widget(Director(name='director'))
        sm.add_widget(Customer(name='customer'))
        sm.add_widget(Operator(name='operator'))
        sm.add_widget(Courier(name='courier'))
        sm.add_widget(HandBooks(name='handbooks'))
        sm.add_widget(Reports(name='reports'))
        sm.add_widget(CustomerOrder(name='customer_order'))
        sm.add_widget(MyOrders(name='my_orders'))
        sm.add_widget(CustomerOrderBasket(name='basket'))
        return sm


if __name__ == '__main__':
    Myapp().run()
