from kivy.config import ConfigParser
from kivy.uix.settings import Settings
from kivy.uix.widget import Widget
from kivy.uix.gridlayout import GridLayout
from kivy.properties import StringProperty
from kivy.app import App
from kivy.uix.screenmanager import Screen
from kivy.core.image import Image as CoreImage
from kivy.uix.image import Image
from kivy.clock import Clock

import mocks

import logging
import re

log = logging.getLogger("photobooth")
log.level = logging.INFO

class MenuScreen(Screen):
    pass
cam = mocks.PhotoBoothCamera()

class PhotoboothPreview(Screen):
    image_name = StringProperty("")
    def __init__(self, **kwargs):
        super(PhotoboothPreview, self).__init__(**kwargs)
        Clock.schedule_interval(self.update_image, 0.5)

    def set_image_name(self, image_name):
        self.image_name = image_name

    def update_image(self, instance):
        self.set_image_name(cam.generate_preview())

class VisualLog(GridLayout, logging.Handler):
    output = StringProperty('')
    def __init__(self, level=logging.NOTSET, **kwargs):
        super(VisualLog, self).__init__(**kwargs)
        logging.Handler.__init__(self)
        log.addHandler(self)
        self.setFormatter("'%(asctime)s-[%(levelname)s][%(name)s]--%(message)s'")

        
    def emit(self, record):
        "using the Clock module for thread safety with kivy's main loop"
        self.output += self.format(record) #"use += to append..."
    
    def format(self, logRecord):
        return "[%s][%s]---%s\n" % (logRecord.levelname, logRecord.name, logRecord.msg)

class SettingsScreen(Screen):
    def __init__(self, **kwargs):
        super(SettingsScreen, self).__init__(**kwargs)
        config = ConfigParser()
        config.read('pi_photobooth/booth_config.ini')

        s = Settings()
        s.add_json_panel('Photo Booth Settings', config, 'pi_photobooth/booth_settings.json')
        self.add_widget(s)
        s.bind(on_close=self.on_close)

    def on_close(self, instance):
        logger = logging.getLogger("photobooth.ui")
        logger.info("Leaving Settings Page")
        self.manager.transition.direction = 'right'
        self.manager.current = "menu"
        pass

class PhotoboothApp(App):

    def on_start(self):
        #TODO do the controller init here.
        pass

if __name__ == '__main__':
    PhotoboothApp().run()
    