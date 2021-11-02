from kivy.properties import ObjectProperty
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.button import MDTextButton, MDFillRoundFlatButton
from kivymd.uix.label import MDLabel
from kivymd.uix.screen import MDScreen
from kivymd.uix.textfield import MDTextField

from Notification import Notification
from WithDB import WithDB
from functools import partial


class HandBooks(MDScreen):

    cont_cities = ObjectProperty(None)
    cont_fleets = ObjectProperty(None)
    cont_services = ObjectProperty(None)
    cont_kinds = ObjectProperty(None)
    titles = []
    dialog = None
    note = Notification(dialog)
    cont = []

    def __init__(self, **kw):
        super().__init__(**kw)
        self.fill_cities()
        self.fill_fleets()
        self.fill_kinds()
        self.fill_services()

    @staticmethod
    def __txt_field(text):
        txt_field = MDTextField()
        txt_field.pos_hint = {'center': .5}
        txt_field.color_mode = 'primary'
        txt_field.mode = 'rectangle'
        txt_field.size_hint_x = None
        txt_field.size_hint_y = None
        txt_field.height = 40
        txt_field.font_size = 20
        txt_field.width = 350
        txt_field.text = text
        return txt_field

    def action_city(self, title, *args):
        city = []
        db_pointer = WithDB()
        if not db_pointer.get_smth('get_city_with_title', [title], city):
            self.note.universal_note('Выбрнного Вами города не существует...', [])
        else:
            self.cont.clear()
            self.cont.append(MDBoxLayout(
                height='110dp',
                orientation='vertical',
                size_hint_y=None)
            )
            title = city[0][0]
            self.cont[0].add_widget(MDFillRoundFlatButton(text='Изменить запись',
                                              on_press=partial(self.change_record, 'alter_city', title)))
            for i in range(1, len(city[0])):
                self.cont[0].add_widget(self.__txt_field(str(city[0][i])))
            self.note.note_with_container(self.cont)

    def action_fleet(self, title, *args):
        fleet = []
        db_pointer = WithDB()
        if not db_pointer.get_smth('get_fleet_with_title', [title], fleet):
            self.note.universal_note('Выбрнного Вами парка не существует...', [])
        else:
            self.cont.clear()
            self.cont.append(MDBoxLayout(
                height='370dp',
                orientation='vertical',
                size_hint_y=None)
            )
            title = fleet[0][0]
            self.cont[0].add_widget(MDFillRoundFlatButton(text='Изменить запись',
                                                          on_press=partial(self.change_record, 'alter_fleet', title)))
            for i in range(1, len(fleet[0])):
                self.cont[0].add_widget(self.__txt_field(str(fleet[0][i])))
            self.note.note_with_container(self.cont)

    def action_kind(self, title, *args):
        kind = []
        db_pointer = WithDB()
        if not db_pointer.get_smth('get_kind_with_title', [title], kind):
            self.note.universal_note('Выбрнного Вами вида транспорта не существует...', [])
        else:
            self.cont.clear()
            self.cont.append(MDBoxLayout(
                height='310dp',
                orientation='vertical',
                size_hint_y=None)
            )
            title = kind[0][0]
            self.cont[0].add_widget(MDFillRoundFlatButton(text='Изменить запись',
                                                          on_press=partial(self.change_record, 'alter_transports_kind', title)))
            for i in range(1, len(kind[0])):
                self.cont[0].add_widget(self.__txt_field(str(kind[0][i])))
            self.note.note_with_container(self.cont)

    def action_service(self, title, *args):
        service = []
        db_pointer = WithDB()
        if not db_pointer.get_smth('get_service_with_title', [title], service):
            self.note.universal_note('Выбрнной Вами услуги не существует...', [])
        else:
            self.cont.clear()
            self.cont.append(MDBoxLayout(
                height='310dp',
                orientation='vertical',
                size_hint_y=None)
            )
            title = service[0][0]
            self.cont[0].add_widget(MDFillRoundFlatButton(text='Изменить запись',
                                                          on_press=partial(self.change_record, 'alter_service', title)))
            for i in range(1, len(service[0])):
                self.cont[0].add_widget(self.__txt_field(str(service[0][i])))
            self.note.note_with_container(self.cont)

    def change_record(self, query, title, *args):
        collection = []
        for child in self.cont[0].children:
            if isinstance(child, MDTextField):
                collection.append(child.text)
        collection.reverse()
        collection.append(title)
        db_pointer = WithDB()
        print(collection)
        if not db_pointer.insert_delete_alter_smth(query, collection):
            return None

    def fill_cities(self, *args):
        self.cont_cities.clear_widgets()
        self.titles.clear()
        db_pointer = WithDB()
        cities = []
        if not db_pointer.get_smth('get_city_titles', [], cities):
            self.cont_cities.add_widget(MDLabel(text='Список пуст.'))
        else:
            for i in range(len(cities)):
                self.titles.append(cities[i][0])
                self.cont_cities.add_widget(MDTextButton(text=cities[i][0],
                                                         heigh=80,
                                                         font_size='30sp',
                                                         on_press=partial(self.action_city, cities[i][0]),
                                                         pos_hint={"center_x": .5, "center_y": .5}
                                                         )
                                            )

    def fill_fleets(self, *args):
        self.cont_fleets.clear_widgets()
        self.titles.clear()
        db_pointer = WithDB()
        fleets = []
        if not db_pointer.get_smth('get_fleet_titles', [], fleets):
            self.cont_fleets.add_widget(MDLabel(text='Список пуст.'))
        else:
            for i in range(len(fleets)):
                self.titles.append(fleets[i][0])
                self.cont_fleets.add_widget(MDTextButton(text=fleets[i][0],
                                                         heigh=80,
                                                         font_size='30sp',
                                                         on_press=partial(self.action_fleet, fleets[i][0]),
                                                         pos_hint={"center_x": .5, "center_y": .5}
                                                         )
                                            )

    def fill_kinds(self, *args):
        self.cont_kinds.clear_widgets()
        self.titles.clear()
        db_pointer = WithDB()
        kinds = []
        if not db_pointer.get_smth('get_kind_titles', [], kinds):
            self.cont_kinds.add_widget(MDLabel(text='Список пуст.'))
        else:
            for i in range(len(kinds)):
                self.titles.append(kinds[i][0])
                self.cont_kinds.add_widget(MDTextButton(text=kinds[i][0],
                                                         heigh=80,
                                                         font_size='30sp',
                                                         on_press=partial(self.action_kind, kinds[i][0]),
                                                         pos_hint={"center_x": .5, "center_y": .5}
                                                         )
                                            )

    def fill_services(self, *args):
        self.cont_services.clear_widgets()
        self.titles.clear()
        db_pointer = WithDB()
        services = []
        if not db_pointer.get_smth('get_service_titles', [], services):
            self.cont_services.add_widget(MDLabel(text='Список пуст.'))
        else:
            for i in range(len(services)):
                self.titles.append(services[i][0])
                self.cont_services.add_widget(MDTextButton(text=services[i][0],
                                                           heigh=80,
                                                           font_size='30sp',
                                                           on_press=partial(self.action_service, services[i][0]),
                                                           pos_hint={"center_x": .5, "center_y": .5}
                                                           )
                                            )

    def load_data(self, *args):
        self.fill_services()
        self.fill_kinds()
        self.fill_cities()
        self.fill_fleets()
