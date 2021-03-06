import logging
from os import path

from kivy.clock import Clock
from kivy.config import ConfigParser
from kivy.core.image import Image as CoreImage
from kivy.graphics.texture import Texture
from kivy.uix.label import Label
from kivy.uix.widget import Widget
from kivy.uix.image import Image
from kivy.uix.relativelayout import RelativeLayout
from kivy.properties import StringProperty, ListProperty, NumericProperty, ObjectProperty
from kivygallery.gallery.screens import ScreenMgr
from kivygallery.gallery.mediafactory import loadMedia, loadPictures

from ui.util import utils
from ui.util.settings import SettingsBase
from preview import Previewer
from background.actions import Actions
import tests.mocks as mocks

from PIL import Image as PILImage
import io

import queue

log = logging.getLogger("photobooth")

class GalleryWidget(RelativeLayout, SettingsBase):
    image_names = ListProperty([])
    focus = StringProperty('')
    media = ListProperty()
    def __init__(self, **kwargs):
        super(GalleryWidget, self).__init__(**kwargs)
        SettingsBase.__init__(self, "pi_photobooth/booth_config.ini")

    def load(self):
        folder_name = self.config.get("Settings", "folder_name")
        #parse folder tree
        mediaDir = path.realpath(".")
        if path.exists(folder_name):
            mediaDir = path.realpath(folder_name)
            self.media = loadPictures(mediaDir)

    def unload(self):
        self.media = []

    def on_image_names(self, instance, image_names):
        #Clear existing grids and reload for now, we can keep them loaded later
        self.clear_widgets()
        for name in self.image_names:
            smart_tile = SmartTile(allow_stretch=False, mipmap=True, source=name)
            smart_tile.bind(on_touch_up=self.select)
            self.add_widget(SmartTile(allow_stretch=False, mipmap=True, source=name))
        pass
    def select(self, instance, value):
        pass
    def fullscreen(self):
        pass
    def exit_fullscreen(self):
        pass

class MemoryImage(Image):
    """Display an image already loaded in memory."""
    memory_data = ObjectProperty(None)

    def __init__(self,**kwargs):
        super(MemoryImage, self).__init__(**kwargs)

    def blackout(self):
        self.texture = Texture.create(self.size)

    def on_memory_data(self, *args):
        """Load image from memory."""
        data = self.memory_data
        if not data:
             log.debug("No data, showing blank");
             self.blackout()
        if data != '':
            with self.canvas:
                if not self.memory_data:
                    log.debug("No data, showing blank")
                    self.blackout()
                    return
                byte_array = data
                byte_array.seek(0)
                img = CoreImage(byte_array, ext="jpg")
                byte_array.flush();
                self.texture = img.texture


class VisualLog(RelativeLayout, logging.Handler):
    output = StringProperty('')
    def __init__(self, level=logging.NOTSET, **kwargs):
        super(VisualLog, self).__init__(**kwargs)
        
        logging.Handler.__init__(self)
        log.addHandler(self)
        self.setFormatter("'%(asctime)s-[%(levelname)s][%(name)s]--%(message)s'")
        self.config = ConfigParser.get_configparser("photobooth_settings")
        if not self.config:
            self.config = ConfigParser("photobooth_settings")
        self.config.read("pi_photobooth/booth_config.ini")
        log.setLevel(self.config.get("Global", "visual_log_level"))

        self.config.add_callback(self.settings_updated)

    def settings_updated(self, section, key, value):
        if section == "Global" and key == "visual_log_level":
            log_level = value
            log.setLevel(log_level)

    def emit(self, record):
        "using the Clock module for thread safety with kivy's main loop"
        self.output += self.format(record) #"use += to append..."
    
    def format(self, logRecord):
        return "[%s][%s]---%s\n" % (logRecord.levelname, logRecord.name, logRecord.msg)

class PhotoboothPreview(RelativeLayout):
    "Updates by name, possible source of performance gain."
    image_data = ObjectProperty("")
    def __init__(self, **kwargs):
        super(PhotoboothPreview, self).__init__(**kwargs)
        self.cam = mocks.PhotoBoothCamera()
        self.previewer = Previewer()
        self.previewing = None
        
        memoryImage = MemoryImage()
        self.bind(image_data=memoryImage.setter("memory_data"))
        self.add_widget(memoryImage)

    def preview(self, generator=None):
        log.debug("Starting Preview")
        if not generator:
            log.info("Creating Generator from Camera")
            generator = self.cam.generate_preview()
        self.image_generator = self.previewer.producer(generator)
        self.previewing = Clock.schedule_interval(self.update_image, 1 / 30)
        
    def review(self, image_name):
        log.debug(f"Reviewing {image_name}")
        image = PILImage.open(image_name)
        image = image.resize((800,480))
        byte_array = io.BytesIO()
        image.save(byte_array, format="jpeg")
        byte_array.seek(0)
        self.image_data = byte_array;
        log.debug(f"Showing {self.image_data}")

    def stop_preview(self):
        log.debug("Stopping Preview")
        if self.previewing:
            self.previewing.cancel()
        self.set_image('')

    def set_image(self, image):
        self.image_data = image
        log.debug(f" Showing {self.image_data}")


    def update_image(self, instance):
        try:
            img = next(self.image_generator)
            self.set_image(img)
        except StopIteration:
            self.previewing.cancel()

class ActionsQueue(RelativeLayout):
    "Updates by name, possible source of performance gain."
    def __init__(self, **kwargs):
        super(ActionsQueue, self).__init__(**kwargs)
        self.queue = queue.Queue()
        self.actions = Actions()

    def push(self, action_name, image_arr):
        "Push a new action to perform onto a queue to process (name, images)"
        pass
    def run_action(self, action_name, image_arr):
        combined_image_name = self.actions.combine(self, image_arr)
        post_id = self.actions.upload("fb", combined_image_name, {"event_name":"fb_event"})
        return post_id
class Countdown(RelativeLayout):
    starting_number = NumericProperty(0)
    current = NumericProperty(-1)
    def __init__(self, starting_number=0, **kwargs):
        super(Countdown, self).__init__(**kwargs)
        self.starting_number = starting_number
        self.event = None
        self.generator = None

    def countdown(self, seconds=None, callback=None):
        if not seconds:
            seconds = self.starting_number
        self.generator = utils.count_down(seconds)
        self.callback = callback
        self.event = Clock.schedule_interval(self.update_count, 0.2)

    def reset(self):
        self.current = -1

    def stop_countdown(self):
        if self.event:
            self.event.cancel()
        self.reset()

    def set_image_name(self, image_name):
        self.image_name = image_name

    def update_count(self, instance):
        if self.generator == None:
            return
        try:
            self.current = next(self.generator)
            if self.current < 0:
                if self.callback:
                    self.callback()
                return False
        except StopIteration as si:
            log.error("Received Stop Iteration before time was up")
            return False
