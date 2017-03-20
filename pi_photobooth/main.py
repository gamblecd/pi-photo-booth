import logging
import re

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
        
    def on_start(self):
        #TODO do the controller init here.
        pass

if __name__ == '__main__':
    PhotoboothApp().run()
