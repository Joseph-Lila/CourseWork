from kivymd.uix.button import MDFlatButton
from kivymd.uix.dialog import MDDialog


class Notification:
    def __init__(self, dialog):
        self.dialog = dialog

    def dialog_close(self, *args):
        self.dialog.dismiss(force=True)

    def universal_note(self, title, params, *args):
        for i in range(len(params)):
            params[i].text = ''
        self.dialog = MDDialog(
            title='Внимание!',
            text=title,
            buttons=[
                MDFlatButton(
                    text='OK',
                    on_release=self.dialog_close
                )
            ],
            size_hint=(0.6, 0.6)
        )
        self.dialog.open()

    def note_with_container(self, cont, title, *args):
        self.dialog = MDDialog(
            title=title,
            type="custom",
            content_cls=cont[0],
            buttons=[
                MDFlatButton(
                    text='Выйти',
                    on_release=self.dialog_close
                )
            ],
            size_hint=(0.9, 0.6)
        )
        self.dialog.open()
