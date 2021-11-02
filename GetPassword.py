from kivy.properties import ObjectProperty
from kivymd.uix.screen import MDScreen

from Notification import Notification


class GetPassword(MDScreen):
    phone = ObjectProperty(None)
    email = ObjectProperty(None)
    dialog = None
    note = Notification(None)

    def dialog_close(self, *args):
        self.dialog.dismiss(force=True)

    def send_password(self):
        if self.phone.text == '' or self.email.text == '':
            self.note.universal_note('Не все поля заполнены!', [])
        else:
            self.note.universal_note('На указанную почту и телефон \nбыли высланы необходимые данные!', [])
