from kivy.clock import Clock
from kivy.config import ConfigParser
from kivy.properties import StringProperty
from kivy.uix.image import Image
from kivy.uix.screenmanager import Screen
from kivy.uix.settings import Settings

import tests.mocks as mocks


class MenuScreen(Screen):
    pass


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


class PhotoboothPreview(Screen):
    "Updates by name, possible source of performance gain."
    image_name = StringProperty("")
    def __init__(self, **kwargs):
        super(PhotoboothPreview, self).__init__(**kwargs)
        self.cam = mocks.PhotoBoothCamera()

        Clock.schedule_interval(self.update_image, 0.5)

    def set_image_name(self, image_name):
        self.image_name = image_name

    def update_image(self, instance):
        img = self.cam.generate_preview()
        self.set_image_name(img.filename)

