from kivy.properties import ObjectProperty
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.button import MDTextButton, MDFillRoundFlatButton
from kivymd.uix.label import MDLabel
from kivymd.uix.screen import MDScreen
from kivymd.uix.textfield import MDTextField

from DbOperator import DbOperator
from Notification import Notification
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

    def on_enter(self, *args):
        self.load_data()

    @staticmethod
    def __txt_field(text, helper_text, disabled):
        txt_field = MDTextField()
        if disabled:
            txt_field.disabled = True
        txt_field.pos_hint = {'center': .5}
        txt_field.color_mode = 'primary'
        txt_field.helper_text = helper_text
        txt_field.helper_text_mode = 'persistent'
        txt_field.mode = 'rectangle'
        txt_field.size_hint_x = None
        txt_field.size_hint_y = None
        txt_field.height = 40
        txt_field.font_size = 20
        txt_field.width = 350
        txt_field.write_tab = False
        txt_field.text = text
        return txt_field

    def any_action(self, entity_func, alter_func, title, height, helper_text_collection, *args):
        entity = entity_func(title)
        if len(entity[-1]) == 0:
            self.note.universal_note('Выбрнной Вами сущности не существует...', [])
        else:
            self.cont.clear()
            self.cont.append(MDBoxLayout(
                height=str(height) + 'dp',
                orientation='vertical',
                size_hint_y=None)
            )
            self.cont[0].add_widget(MDFillRoundFlatButton(text='Изменить запись',
                                                          on_press=partial(self.change_record, alter_func)
                                                          )
                                    )
            self.cont[0].add_widget(self.__txt_field(str(entity[0][0])+". "+str(entity[1][0]),
                                                     helper_text_collection[0], True))
            for i in range(len(entity[0]) - 1):
                self.cont[0].add_widget(self.__txt_field(str(entity[0][i+1]), helper_text_collection[i+1], False))
            self.note.note_with_container(self.cont, 'Окно редактирования', (.9, .6))

    def change_record(self, changes_func, *args):
        collection = [child.text for child in self.cont[0].children if isinstance(child, MDTextField)]
        collection.reverse()
        col1 = [collection[0].split(". ")[0]]
        col2 = [collection[0].split(". ")[1]]
        for i in range(len(collection) - 1):
            col1.append(collection[i+1])
            col2.append(collection[i+1])
        collection.clear()
        collection.append(col1)
        collection.append(col2)
        changes_func(collection)

    def fill_any_department(self, cont, data_func, on_press_func, entity_func, alter_func, height,
                            helper_text_collection):
        cont[-1].clear_widgets()
        self.titles.clear()
        data_collection = data_func()
        if len(data_collection) == 0:
            cont[-1].add_widget(MDLabel(text='Список пуст.'))
        else:
            for item in data_collection:
                self.titles.append(item)
                cont[-1].add_widget(MDTextButton(text=item,
                                                 heigh=80,
                                                 font_size='30sp',
                                                 on_press=partial(on_press_func, entity_func, alter_func, item, height,
                                                                  helper_text_collection),
                                                 pos_hint={"center_x": .5, "center_y": .5}
                                                 )
                                    )

    def load_data(self, *args):
        if not DbOperator().try_connection():
            self.note.universal_note('Нет соединеня с одной из БД!', [])
            return
        self.fill_any_department([self.cont_services],
                                 DbOperator().get_service_titles,
                                 self.any_action,
                                 DbOperator().get_service_fields_with_title,
                                 DbOperator().alter_service_using_str_collection,
                                 330,
                                 ('service_id', 'title', 'description', 'cost_weight', 'cost_radius')
                                 )
        self.fill_any_department([self.cont_kinds],
                                 DbOperator().get_kind_titles,
                                 self.any_action,
                                 DbOperator().get_kind_fields_with_title,
                                 DbOperator().alter_kind_using_str_collection,
                                 330,
                                 ('kind_id', 'description', 'title', 'lifting_capacity', 'volume')
                                 )
        self.fill_any_department([self.cont_cities],
                                 DbOperator().get_city_titles,
                                 self.any_action,
                                 DbOperator().get_city_fields_with_title,
                                 DbOperator().alter_city_using_str_collection,
                                 150,
                                 ('city_id', "title")
                                 )
        self.fill_any_department([self.cont_fleets],
                                 DbOperator().get_fleet_titles,
                                 self.any_action,
                                 DbOperator().get_fleet_fields_with_title,
                                 DbOperator().alter_fleet_using_str_collection,
                                 430,
                                 ('title', 'description', 'address', 'square', 'stars_quantity')
                                 )
