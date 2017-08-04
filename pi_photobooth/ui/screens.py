from kivy.config import ConfigParser
from kivy.properties import StringProperty,ListProperty
from kivy.uix.image import Image
from kivy.uix.screenmanager import Screen
from kivy.uix.settings import Settings
from .events import PhotoboothEventDispatcher
from background.actions import Actions
import tests.mocks as mocks

from ui.util.settings import SettingsBase
import models
import logging
import os
from pathlib import Path

class MenuScreen(Screen):
    pass

class SettingsScreen(Screen):
    init = False
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
        s.add_json_panel('Cognitive Services', config, 'pi_photobooth/cognitive_services.json')
        self.add_widget(s)
        
    def on_pre_leave(self):
        logger = logging.getLogger("photobooth.ui")
        logger.debug("Leaving Settings Page")
        pass

    def on_enter(self):
        logger = logging.getLogger("photobooth.screenmanager")
        logger.debug("Entering Settings Page")

class PhotoboothScreen(Screen, SettingsBase):
    def __init__(self, **kwargs):
        self.logger = logging.getLogger("photobooth.screenmanager.booth")
        SettingsBase.__init__(self, "pi_photobooth/booth_config.ini")
        
        super(PhotoboothScreen, self).__init__(**kwargs)

        if self.config.get("Global", "testing") == "1":
            self.logger.info("Using Mock data, providing mock Camera")
            self.cam = mocks.PhotoBoothCamera()
        else:
            self.cam = models.PhotoBoothCamera()
            self.cam.init()
        self.photobooth_events = PhotoboothEventDispatcher()
      
    def on_parent(self, instance, something):
        pass
        #self.ids["preview"].preview(self.cam.generate_preview())

    def on_enter(self):
        self.logger.info("Entering {}".format(self.name))

    def on_pre_leave(self):
        self.reset()
        self.logger.info("Leaving {}".format(self.name))

    def hide_shoot_button(self):
        self.ids["shoot_button"].opacity = 0
        self.ids["shoot_button"].disabled = True

    def show_shoot_button(self):
        self.ids["shoot_button"].opacity = 1.
        self.ids["shoot_button"].disabled = False

    def on_change_state(self, current_state, state_data):
        new_state = current_state.next_state(state_data)
        if not new_state:
            self.photobooth_events.dispatch("on_complete_all")
            return
        new_state.run(state_data, self)

    def reset(self):
        self.ids["preview"].stop_preview()
        self.ids["countdown"].stop_countdown()
        self.show_shoot_button()
        pass
   
    def run_booth(self):
        self.hide_shoot_button()
        booth_images = BoothData(self.config, self.on_change_state)
        frame_count = self.config.getint("Settings", "frame_count")
        booth_images["frame_count"] = frame_count
        self.logger.info(f"Taking {frame_count} pictures")

        InitialState.run(booth_images, self)
    
    def run_preview(self, seconds=4, callback=None):
        self.logger.info(f"Run Preview for {seconds} seconds.")
        def cb():
            self.ids["preview"].stop_preview()
            if callback:
                callback()
        self.ids["preview"].preview(generator=self.cam.generate_preview())
        self.ids["countdown"].countdown(seconds, callback=cb)

    def run_review(self, image_name, seconds=2, callback=None):
        self.logger.info(f"Showing review for {seconds} seconds.")
        def cb():
            self.ids["preview"].stop_preview()
            if callback:
                callback()
        self.ids["preview"].review(image_name)
        self.ids["countdown"].countdown(seconds, callback=cb)

    def take_picture(self):
        self.logger.info("Performing image capture")
        self.cam.focus()
        file_data = self.cam.capture()
        folder_name = self.config.get("Settings", "folder_name")
        local_file = self.save(file_data, folder_name=folder_name)
        self.photobooth_events.captured(local_file)
        return local_file

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
        self.logger.debug(f"Saved {imglocation}")
        return imglocation

class BoothData(dict):
    def __init__(self, config, handle_state_end=None, *args, **kw):
        super(BoothData,self).__init__(*args, **kw)
        self.images = []
        self.settings = config
        self.handle_state_end = handle_state_end

class BoothState():
    def __init__(self):
        self.logger = logging.getLogger("photobooth.booth.state")
    '''
    Initial State:
    No Pictures started
    Previewing
    Taking Picture
    Review

    '''

class EmptyState(BoothState):
    
    def run(state_data, screen):
        screen.reset()
        state_data.handle_state_end(EmptyState, state_data)
        pass
    def next_state(state_data):
        return None

class InitialState(BoothState):

    def run(state_data, screen):
        #Increment this run
        times_through = state_data.get("count")
        if not times_through:
            times_through = 0
        state_data["count"] =  times_through+1
        state_data.handle_state_end(InitialState, state_data)

        
    def next_state(state_data):
        return PreviewState

class PreviewState(BoothState):

    def run(state_data, screen):
        def cb():
            state_data.handle_state_end(PreviewState, state_data)
        screen.run_preview(state_data.settings.getint("Settings", "preview_seconds"), cb)
    def next_state(state_data):
        return CaptureState
        pass            

class CaptureState(BoothState):

    def run(state_data, screen):
        image_name = screen.take_picture()
        state_data["image_name"] = image_name
        screen.logger.info(f"Adding {image_name} to booth_images")
        state_data.images.append(image_name)
        state_data.handle_state_end(CaptureState, state_data)

    def next_state(state_data):
        return ReviewState
        pass            

class ReviewState(BoothState):

    def run(state_data, screen):
        def cb():
            state_data.handle_state_end(ReviewState, state_data)
        screen.run_review(state_data.get("image_name"),state_data.settings.getint("Settings", "review_seconds"), cb)

    def next_state(state_data):
        if state_data["count"] < state_data["frame_count"]:
            #Return preview state
            return InitialState
        else:
            #Return end state
            return ActionState

class ActionState(BoothState):

    def run(state_data, screen):
        screen.logger.info("Running Action State")
        screen.logger.info(str(state_data.images))

        #TODO Actions
        actions = Actions()
        actions.combine_and_upload_to_event(state_data.images, state_data.settings.get("Social", "event_name"))

        state_data.handle_state_end(ActionState, state_data)

    def next_state(state_data):
        return EmptyState

