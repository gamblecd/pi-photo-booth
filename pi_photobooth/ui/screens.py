from kivy.clock import Clock
from kivy.config import ConfigParser
from kivy.properties import StringProperty
from kivy.uix.image import Image
from kivy.uix.screenmanager import Screen
from kivy.uix.settings import Settings

import tests.mocks as mocks

import logging
import os
from pathlib import Path

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

    def on_enter(self):
        logger = logging.getLogger("photobooth.screenmanager")
        logger.info("Nested screen on_enter event")
        logger.info("Entering {}".format(self.name))


class PhotoboothScreen(Screen):
    def __init__(self, **kwargs):
        super(PhotoboothScreen, self).__init__(**kwargs)
        self.cam = mocks.PhotoBoothCamera()
        self.next = None
        self.logger = logging.getLogger("photobooth.screenmanager")

    def on_enter(self):
        # TODO begin process
        #self.ids["preview"].preview(10)
        self.logger.info("Nested screen on_enter event")
        self.logger.info("Entering {}".format(self.name))

    def on_pre_leave(self):
        # TODO end process
        self.ids["preview"].stop_preview()
        self.logger.info("Nested screen on_exit event")
        self.logger.info("Leaving {}".format(self.name))

    def take_picture(self):
        self.logger.info("performing image capture")
        self.cam.focus()
        file_data = self.cam.capture()
        local_file = self.save(file_data)
        return local_file

    def save(self, file_data, folder_name="TEST"):
        cam = self.cam
        img = cam.get_image(file_data)
        imglocation = "{0}/{1}".format(folder_name, file_data.name)
        self.logger.info("Saving Image To {imglocation}")
        img_path = Path(imglocation)
        if not os.path.exists(img_path.parent):
            os.makedirs(img_path.parent)
        if os.path.exists(img_path.parent):
            #TODO RE handle dupse
            imglocation = "{0}/{1}".format(folder_name, file_data.name)
        img.save(imglocation)
        return imglocation

    def reset(self):
        pass

    def run_review(self, image_name, seconds=2):
        self.logger.info("Run Preview for {seconds} seconds.")

        self.ids["preview"].review(image_name)
        def end_countdown():
            self.reset()
        self.ids["countdown"].countdown(seconds, callback=end_countdown)

    def run_preview(self, seconds=4):
        self.logger.info("Run Preview for {seconds} seconds.")

        self.ids["preview"].preview(generator=self.cam.generate_preview())
        def end_countdown():
            self.ids["preview"].stop_preview()
            img = self.take_picture()
            self.run_review(img)
        self.ids["countdown"].countdown(seconds, callback=end_countdown)
