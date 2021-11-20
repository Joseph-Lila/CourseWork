from kivy.properties import ObjectProperty
from kivymd.uix.screen import MDScreen
from ListItemWithCheckbox import ListItemWithCheckbox
from RightCheckbox import RightCheckbox

basket = []


class CustomerOrderBasket(MDScreen):
    container = ObjectProperty(None)

    def __init__(self, **kw):
        super().__init__(**kw)

    def on_enter(self, *args):
        self.add_items_from_basket()

    def go_back(self, *args):
        self.manager.current = 'customer'

    def remove_gui_items(self):
        for item in RightCheckbox.my_collection:
            if item in self.container.children[:]:
                self.container.remove_widget(item)
        RightCheckbox.my_collection.clear()

    def add_items(self, *args):
        self.manager.current = 'customer_order'

    def add_items_from_basket(self, *args):
        self.remove_gui_items()
        for i, item in enumerate(basket, start=1):
            cur_text = f'{i}. {item.title} ({item.begin_city.text} -> {item.end_city.text})'
            self.container.add_widget(ListItemWithCheckbox(text=cur_text))



