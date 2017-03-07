import time
from shutil import copy
import os
class Actions:

    def combine_and_upload_to_event(self, *args):
        print("Combining and uploading imgs: %s" % args)
        pass


class mockImage():

    def __init__(self, filename):
        self.filename=filename
        self.name=filename

    def get_data_and_size(self):
        f = open(self.filename,'rb');
        return f.read()

    def save(self, path):
        copy(os.path.abspath(self.filename), os.path.abspath(path))
        pass

class PhotoBoothContext:
    def getContext(self):
        return {};

class PhotoBoothCamera:

    def __init__(self, context={}):
        self.context = context
        self.initiated = False
        self.generator = None

    def init(self):
        self.initiated = True

    def set_context(self, context):
        self.context = context

    def get_config(self):
        return ()

    def _set_config_value(self, name, value):
        config = self.get_config()
        print("Set %s to %s" % (name, value))

    def _set_viewfinder(self, value):
        self._set_config_value("viewfinder", value)

    def image_format(self):
        return "JPG"

    def wait_for_event(self, timeout, event_type, event_data):
        return {}

    def trigger_capture(self):
        if self.generator is None:
            self.generator = self.frame_gen();
        return next(self.generator)

    def capture(self):
        if self.generator is None:
            self.generator = self.frame_gen();
        return next(self.generator)

    def get_image(self, file):
        if self.generator is None:
            self.generator = self.frame_gen();
        return next(self.generator)

    def generate_preview(self):
        if self.generator is None:
            self.generator = self.frame_gen();
        while True:
            yield next(self.generator)

    def frame_gen(self):
        m1 = mockImage("pi_photobooth/tests/imgs/test.jpg")
        m2 = mockImage("pi_photobooth/tests/imgs/test1.png")
        while True:
            if int(time.time()) % 2 == 0:
                yield m1
            else:
                yield m2

    
    def capture_preview(self):
        if self.generator is None:
            self.generator = self.frame_gen();
        return self.generator.next()

    def capture_movie(self):
        #TODO return 
        return []
        #return self.camera.capture(gp.GP_CAPTURE_MOVIE, self.context)

    def focus(self, distance=None):
        if distance is None:
            #Turn mirror down, set autofocus
            self.mirror_down()
            self._set_config_value("autofocusdrive", 1)
            # Focus will happen before shoot
        else:
            #Need to set preview mode of not available
            config = self.get_config()
            config.set("manualfocusdrive", distance)

    def mirror_up(self):
        print("Mirror Top")

    def mirror_down(self):
        print("Mirror Down")

    def destroy(self):
        pass
