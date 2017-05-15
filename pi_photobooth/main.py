import logging
import re
import cProfile

from kivymd.theming import ThemeManager
from kivy.app import App
from kivy.clock import Clock
from kivy.config import Config, ConfigParser
from kivy.properties import StringProperty, NumericProperty
from kivy.uix.gridlayout import GridLayout
from kivy.uix.image import Image
from kivy.uix.screenmanager import Screen
from kivy.uix.settings import Settings
from kivy.config import ConfigParser

from ui.widgets import *
from ui.screens import *

class PhotoboothApp(App): 
    theme_cls = ThemeManager()
    def __init__(self, **kwargs):
        super(PhotoboothApp, self).__init__(**kwargs)
        
    # def on_start(self):
    #     self.profile = cProfile.Profile()
    #     self.profile.enable()

    # def on_stop(self):
    #     self.profile.disable()
    #     self.profile.dump_stats('myapp.profile')
if __name__ == '__main__':
    PhotoboothApp().run()
