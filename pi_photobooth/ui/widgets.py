import logging 

from kivy.clock import Clock
from kivy.core.image import Image as CoreImage
from kivy.uix.widget import Widget
from kivy.core.image.img_pil import ImageLoaderPIL
from kivy.uix.image import Image
from kivy.uix.gridlayout import GridLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.properties import StringProperty,NumericProperty, ObjectProperty
from ui.util import utils
from preview import Previewer
import tests.mocks as mocks

log = logging.getLogger("photobooth")
log.level = logging.INFO


class MemoryImage(Image):
    """Display an image already loaded in memory."""
    memory_data = ObjectProperty("")

    def __init__(self,**kwargs):
        super(MemoryImage, self).__init__(**kwargs)

    def on_memory_data(self, *args):
        """Load image from memory."""
        with self.canvas:
            self.memory_data.seek(0)
            im = CoreImage(self.memory_data, ext='jpg')
            tex = im.texture
            self.texture = tex



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

class PhotoboothPreview(BoxLayout):
    "Updates by name, possible source of performance gain."
    image_name = ObjectProperty("")
    def __init__(self, **kwargs):
        super(PhotoboothPreview, self).__init__(**kwargs)
        self.cam = mocks.PhotoBoothCamera()
        self.previewer = Previewer()

    def preview(self, generator=None):
        log.info("Starting Preview")
        if not generator:
            log.info("Creating Generator from Camera")
            generator = self.cam.generate_preview()
        self.image_generator = self.previewer.producer(generator)
        self.previewing = Clock.schedule_interval(self.update_image, 0.3)
        
    def review(self, image_name):
        f = open(image_name,'rb');
        self.image_name =  self.previewer.produce_frame(f.read())

    def stop_preview(self):
        log.info("Stopping Preview")
        if self.previewing:
            self.previewing.cancel()

    def set_image_name(self, image_name):
        self.image_name = image_name

    def update_image(self, instance):
        try:
            img = next(self.image_generator)
            self.set_image_name(img)
        except StopIteration:
            self.previewing.cancel();

class PhotoboothReview(BoxLayout):
    "Updates by name, possible source of performance gain."
    image = ObjectProperty("")
    def __init__(self, **kwargs):
        super(PhotoboothReview, self).__init__(**kwargs)

    def set_image(self, image_data):
        self.image = image_data

class Countdown(BoxLayout):
    starting_number = NumericProperty(0)
    current = NumericProperty(0)
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

    def set_image_name(self, image_name):
        self.image_name = image_name

    def update_count(self, instance):
        if self.generator == None:
            return
        self.current = next(self.generator)
        if self.current <= 0:
            if self.callback:
                self.callback()
            return False
