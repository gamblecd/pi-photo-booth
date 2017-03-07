from kivy.event import EventDispatcher


class PhotoboothEventDispatcher(EventDispatcher):
    def __init__(self, **kwargs):
        self.register_event_type("on_capture")
        self.register_event_type("on_countdown")
        self.register_event_type("on_complete_once")
        self.register_event_type("on_complete_all")
        super(PhotoboothEventDispatcher, self).__init__(**kwargs)

    def on_complete_all(self, args):
        pass
    def on_complete_once(self):
        pass
    def on_capture(self, image_name):
        pass
    def on_countdown(self):
        pass

    def all_completed(self, images):
        self.dispatch("on_complete_all", images)

    def once_completed(self):
        self.dispatch("on_complete_once")
    def countdown_ended(self):
        self.dispatch("on_countdown")
    def captured(self, image_name):
        self.dispatch("on_capture", image_name)