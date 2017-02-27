import logging 
from kivy.clock import Clock
from kivy.uix.widget import Widget
from kivy.uix.gridlayout import GridLayout
from kivy.properties import StringProperty,NumericProperty
from ui.util import utils
log = logging.getLogger("photobooth")
log.level = logging.INFO

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


class Countdown(Widget):
    "Updates by name, possible source of performance gain."
    starting_number = NumericProperty(0)
    current = NumericProperty(0)
    def __init__(self, starting_number=0, **kwargs):
        super(Countdown, self).__init__(**kwargs)
        self.starting_number = starting_number
        self.event = Clock.schedule_interval(self.update_count, 0.2)
        self.event.cancel()

    def on_starting_number(self, instance, value):
        self.generator = utils.count_down(value)
        self.event()

    def set_image_name(self, image_name):
        self.image_name = image_name

    def update_count(self, instance):
        if self.generator == None:
            return
        self.current = next(self.generator)
        if self.current <= 0:
            self.event.cancel()
            self.generator = None
