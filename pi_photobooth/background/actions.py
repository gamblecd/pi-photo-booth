from .social.facebook_uploader import FacebookUploader
from .image import ImageProcessor, Directions
import tests.mocks as mocks
import logging
from kivy.config import ConfigParser
from ui.util.settings import SettingsBase

class Actions(SettingsBase):
    def __init__(self, uploader=None, image_proc=ImageProcessor()):
        self.logger = logging.getLogger("photobooth.actions")
        self.logger.info("Loading Actions")
        super(Actions, self).__init__('pi_photobooth/booth_config.ini')
        self.image_processor = image_proc
        self.settings_updated("Global", "testing", self.config.getboolean("Global", "testing"));
        self.logger.info("Actions Loaded")
        
    def settings_updated(self, section, key, value):
        if section == "Global" and key == "testing":
            is_testing = bool(int(value))
            self.logger.info(f"Setting Social Action usage to {is_testing}")
            if not is_testing:
                self.fb = FacebookUploader()
            else:
                self.fb = mocks.FacebookUploader()

    def define_name(self, img_arr):
        if not img_arr:
            return ""
        return "{}_photoBooth.jpg".format(img_arr[0].split(".")[0])

    def combine(self, img_arr, direction=Directions.VERTICAL):
        image_name = self.define_name(img_arr)
        self.logger.debug(f"Combining {len(img_arr)} images into one {direction} named: {image_name}")
        return self.image_processor.combine(img_arr, image_name, Directions.VERTICAL)

    def upload(self, social_outlet, image_name, options={}):
        if social_outlet is "fb":  
            self.logger.debug(f"Beginning upload to facebook with options {options}")
            event_name = options["event_name"]
            if not event_name:
                self.logger.warning(f"No 'event_name' found in {options}. Skipping upload.")
                return
            self.logger.info(f"Grabbing Event Id for {event_name}")
            try:
                event_id = self.fb.event(event_name)
                #TODO progress bar?
                post_id = self.fb.upload_to_event(image_name, event_id).get("post_id")
                self.logger.info("Uploaded...")
                return post_id
            except Exception as e:
                self.logger.error(f"Upload failed, message was {e}")
            return ""
    def combine_and_upload_to_event(self, img_arr, event_name):
        if not img_arr:
            return ""
        self.logger.info("Grabbing Event Id")
        event_id = self.fb.event(event_name);

        print("Processing Image")
        image_name = self.define_name(img_arr)
        new_img_name = self.image_processor.combine(img_arr, image_name, Directions.VERTICAL)

        print("Uploading new Image to Event")
        post_id = self.fb.upload_to_event(new_img_name, event_id).get("post_id")
        print("Uploaded...")
        return post_id