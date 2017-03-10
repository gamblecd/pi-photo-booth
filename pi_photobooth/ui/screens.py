from kivy.clock import Clock
from kivy.config import ConfigParser
from kivy.properties import StringProperty
from kivy.uix.image import Image
from kivy.uix.screenmanager import Screen
from kivy.uix.settings import Settings

from .events import PhotoboothEventDispatcher
from background.actions import Actions
import tests.mocks as mocks

from ui.util.settings import SettingsBase
import logging
import os
from pathlib import Path

class MenuScreen(Screen):
    pass

class SettingsScreen(Screen):
    def __init__(self, **kwargs):
        super(SettingsScreen, self).__init__(**kwargs)
        config = ConfigParser.get_configparser("photobooth_settings")
        if not config:
            config = ConfigParser(name="photobooth_settings")
        config.read('pi_photobooth/booth_config.ini')

        s = Settings()
        s.add_json_panel('Photo Booth Settings', config, 'pi_photobooth/booth_settings.json')
        s.add_json_panel('Social Media Settings', config, 'pi_photobooth/social_settings.json')
        s.add_json_panel('Testing Settings', config, 'pi_photobooth/testing_settings.json')
        self.add_widget(s)
        s.bind(on_close=self.on_close)

    def on_close(self, instance):
        logger = logging.getLogger("photobooth.ui")
        logger.debug("Leaving Settings Page")
        self.manager.transition.direction = 'right'
        self.manager.current = "menu"
        pass

    def on_enter(self):
        logger = logging.getLogger("photobooth.screenmanager")
        logger.debug("Entering Settings Page")


class PhotoboothScreen(Screen, SettingsBase):
    def __init__(self, **kwargs):
        self.logger = logging.getLogger("photobooth.screenmanager.booth")
        SettingsBase.__init__(self, "pi_photobooth/booth_config.ini")
        
        super(PhotoboothScreen, self).__init__(**kwargs)
    
        self.cam = mocks.PhotoBoothCamera()
        self.next = None
        self.actions = Actions()
        self.photobooth_events = PhotoboothEventDispatcher()
        #When we capture an image, we want to review it 
        self.photobooth_events.bind(on_capture=self.run_review, on_countdown=self.countdown_ended)

    def on_enter(self):
        # TODO begin process
        self.logger.info("Entering {}".format(self.name))

    def on_pre_leave(self):
        # TODO end process
        self.ids["preview"].stop_preview()
        self.ids["countdown"].stop_countdown()
        self.logger.info("Leaving {}".format(self.name))

    def take_picture(self):
        self.logger.info("Performing image capture")
        self.cam.focus()
        file_data = self.cam.capture()
        folder_name = self.config.get("Settings", "folder_name")
        local_file = self.save(file_data, folder_name=folder_name)
        self.photobooth_events.captured(local_file)

    def save(self, file_data, folder_name="TEST"):
        cam = self.cam
        img = cam.get_image(file_data)
        imglocation = "{0}/{1}".format(folder_name, file_data.name)
        self.logger.debug(f"Saving Image To {imglocation}")
        img_path = Path(imglocation)
        if not os.path.exists(img_path.parent):
            os.makedirs(img_path.parent)
        if os.path.exists(img_path.parent):
            #TODO RE handle dupse
            imglocation = "{0}/{1}".format(folder_name, file_data.name)
        img.save(imglocation)
        self.logger.debug("Saved")
        return imglocation


    def run_booth(self):
        booth_images = BoothData(self.config)
        frame_count = self.config.getint("Settings", "frame_count")
        booth_images["frame_count"] = frame_count
        self.logger.info(f"Taking {frame_count} pictures")
        def appendImage(instance, image_name):
            self.logger.info(f"Adding {image_name} to booth_images")
            booth_images.images.append(image_name)
        def performActions(instance, images):
            #TODO perform actions
            self.logger.info(str(booth_images))
            image_name = self.actions.combine(booth_images.images)
            self.actions.upload("fb", image_name, {"event_name": self.config.get("Social", "event_name")})
            pass
        def on_single_completion(instance):
            nonlocal booth_images 
            booth_images.images
            if len(booth_images.images) < booth_images["frame_count"]:
                self.logger.info(f"Running again count: {len(booth_images.images)}")
                self.run_once()
            else:
                self.photobooth_events.dispatch("on_complete_all", booth_images)
        # Collect Images
        self.photobooth_events.bind(on_capture=appendImage,
                                    on_complete_once=on_single_completion,
                                    on_complete_all=performActions)
        #Step 1 Run the process at least once
        self.run_once()
        pass

    def reset(self):
        pass

    def run_once(self):
        def callback():
            self.ids["preview"].stop_preview()
            self.take_picture()
        self.run_preview(seconds=self.config.getint("Settings", "preview_seconds"), callback=callback)

    def run_review(self, instance, image_name, seconds=2):
        seconds = self.config.getint("Settings", "review_seconds")
        self.logger.info(f"Showing review for {seconds} seconds.")

        self.ids["preview"].review(image_name)
        def end_countdown():
            self.photobooth_events.once_completed()
        self.ids["countdown"].countdown(seconds, callback=end_countdown)

    def countdown_ended(self):
        pass

    def run_preview(self, seconds=4, callback=None):
        self.logger.info(f"Run Preview for {seconds} seconds.")
        self.ids["preview"].preview(generator=self.cam.generate_preview())
        self.ids["countdown"].countdown(seconds, callback=callback)

class BoothData(dict):
    def __init__(self, config, *args, **kw):
        super(BoothData,self).__init__(*args, **kw)
        self.images = []
        self.settings = config

class BoothState():
    '''
    Initial State:
    No Pictures started
    Previewing
    Taking Picture
    Review

    '''

class EmptyState(BoothState):
    
    def run(state_data, screen):
        pass
    def next_state(state_data):
        return InitialState

class InitialState(BoothState):

    def run(state_data, screen):
        #Increment this run
        times_through = state_data.get("count")
        state_data.set("count", times_through+1)

    def next_state(state_data):
        return PreviewState

class PreviewState(BoothState):

    def run(state_data, screen):
        screen.run_preview(state_data.settings.getint("Settings", "preview_seconds"))

    def next_state(state_data):
        return CaptureState
        pass            

class CaptureState(BoothState):

    def run(state_data, screen):
        state_data.set("image_name", screen.take_picture())

    def next_state(state_data):
        return ReviewState
        pass            

class ReviewState(BoothState):

    def run(state_data, screen):
        screen.run_review(state_data.get("image_name"))

    def next_state(state_data):
        if len(state_data.images) > state_data.get("frame_count"):
            #Return preview state
            pass
        else:
            #Return end state
            return ActionState

class ActionState(BoothState):

    def run(state_data, screen):
        pass

    def next_state(state_data):
        return EmptyState

