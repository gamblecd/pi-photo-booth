import re
import cProfile

from kivymd.theming import ThemeManager
from kivy.app import App

from ui.widgets import *
from ui.screens import *


class PhotoboothApp(App):
    theme_cls = ThemeManager()
    def __init__(self, **kwargs):
        super(PhotoboothApp, self).__init__(**kwargs)

    def on_start(self):
        self.profile = cProfile.Profile()
        self.profile.enable()

    def on_stop(self):
        self.profile.disable()
        self.profile.dump_stats('myapp.profile')
if __name__ == '__main__':
    PhotoboothApp().run()
