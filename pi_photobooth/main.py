import re
import cProfile

# config
from kivy.config import Config
Config.set('kivy', 'keyboard_mode', 'systemandmulti') # Allow touch keyboard on tft screen


from kivy.app import App

from ui.widgets import *
from ui.screens import *

SettingsScreen()

class PhotoboothApp(App):
    def __init__(self, **kwargs):
        super(PhotoboothApp, self).__init__(**kwargs)

    def on_start(self):
        self.profile = cProfile.Profile()
        self.profile.enable()

    def on_stop(self):
        self.profile.disable()
        self.profile.dump_stats('myapp.profile')
if __name__ == '__main__':
    should_exit = False
    while not should_exit:
        try:
            PhotoboothApp().run()
            should_exit = True
        except NameError as e:
            print("Caught Major error {}".format(e))