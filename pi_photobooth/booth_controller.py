import pygame
import preview as pv
from outputs import OutputScreen, Surfaces
from enum import Enum
import os
import time
import _thread
import threading
from background import actions
import random
import sys, select

from queue import Queue
from tests import mocks

ONLINE = False
MOCK = True
GPIO = False

if GPIO:
    from inputs import Button

if not MOCK:
    import models

class PhotoBoothController:
    pass

class PhotoBooth:

    def __initActions(self):
        print("loading Actions")
        if ONLINE:
            self.actions = actions.Actions()
        else:
            self.actions = mocks.Actions()
        self.processes = []
        print("loading: Actions -- Complete")

    def __initPreviewer(self):
        print("loading Previewer")
        self.previewer = pv.Previewer(self.screen)
        print("loading: Previewer -- Complete")

    def __initCamera(self):
        print("loading: Camera -- Mock -- Complete")

    @property
    def camera(self):
        if MOCK:
            return {}
        return self._camera

    def __init__(self, screen_widget = None):
        self.screen_widget = screen_widget
        self.init_complete = False
        pass

    def init(self):
        load_event = threading.Event()
        try:
            self.acting = False
            if GPIO:
                self._button = Button()
            self.__initActions()
            self.__initPreviewer()
            self.__initCamera()
            time.sleep(.1)
            self.init_complete = True
        except Exception as e:
            load_event.set()
            print(e)
            self.init_complete = False
        load_event.set()

    def __del__(self):
        if self.processes:
            for p in self.processes:
                if p.isAlive():
                    # TWenty seconds to finish any actions
                    p.join(20)

    #set autofocus, take a frame, ignore picture
    def __updateFocus(self):
        cam = self.camera
        cam.focus()
        cam.capture()

    def save(self, file_data, folderName = "TEST"):
        cam = self.camera
        img = cam.get_image(file_data)
        imglocation = "{0}/{1}".format(folderName, file_data.name)
        print(imglocation)
        if not os.path.exists(folderName):
            os.makedirs(folderName)
        if os.path.exists(imglocation):
            imglocation = "{0}/d_{1}".format(folderName, file_data.name)
        img.save(imglocation)
        return imglocation

    def buttonListener(self, queue, halt_event):

        def callback(ev=None):
            if not halt_event.is_set():
                if not queue.full():
                    try:
                        if self._button.islongPress():
                            queue.put(ThreadEvents.SHUTDOWN, block=False)
                        else:
                            queue.put(ThreadEvents.SHOOTING, block=False)
                    except Queue.Full:
                        print("Ignored input, button")
                else:
                    print("Ignored input, button")
        return callback

    def __wait_for_input(self, timeout=5):
        timer = threading.Timer(timeout, _thread.interrupt_main)
        astring = None
        try:
            timer.start()
            astring = input("")
        except KeyboardInterrupt:
            pass
        timer.cancel()
        if (astring):
            return False, astring
        else:
            return True, None

    def __show_main_screen(self):
        cam = self.camera
        self._print("Press Button to begin taking pictures", erase=True)
        # TODO: undo this
        battery_level = 50;
        if battery_level < 5:
            self.outputScreen.drawText("REPLACE BATTERY NOW!",
                                     location=Surfaces.UP_LEFT)
        else:
            self.outputScreen.drawText("Battery: {}".format(battery_level),
                                     location=Surfaces.UP_LEFT)


    def __start_shoot_set(self, queue, halt_event):
        self.__show_main_screen()
        while not halt_event.is_set():
            event = queue.get()
            queue.put("spacer")
            print("Got Event: {}".format(event))

            if event is ThreadEvents.SHUTDOWN:
                halt_event.set()
                self._print("Shutting Down...", erase=True)
            elif event is ThreadEvents.SHOOTING:
                if not MOCK:
                    self.photo_shoot()
                else:
                    self._boothAction(1)
                self.__show_main_screen()
            queue.task_done()
            queue.get()
            queue.task_done()

    def run(self):
        if not self.init_complete:
            time.sleep(2)
            return
        print("Display Instruction Screen")
        queue = Queue(maxsize=1)

        halt_event = threading.Event()

        if GPIO:
            self._button.listen(self.buttonListener(queue, halt_event))

        keyboard_thread = threading.Thread(target=self.keyboard_listener, args=[queue, halt_event])
        keyboard_thread.start()
        self.processes.append(keyboard_thread)

        self.__start_shoot_set(queue, halt_event)

    def photo_shoot(self, count=4):
        #cam = models.PhotoBoothCamera()
        cam = self.camera
        try:
            # Mirror up and to speed things up, less sounds from camera for usability
            cam.mirror_up()

            images = [self.previewAndSnap() for _ in range(count)]

            cam.mirror_down()

            #Actions with list of 4 photos
            self.performActions(images)
            self.outputScreen.clear()
        except Exception as e:
            self._print("Unknown Error (Aborting Shoot):{}".format(e.message))
        pass

    def _print(self, message, erase=False):
        print(message)
        self.outputScreen.drawText(message, erase=erase)

    def _addCompliment(self):
        surface = random.choice([Surfaces.DOWN_LEFT, Surfaces.UP_LEFT, Surfaces.UP_RIGHT, Surfaces.LEFT_SIDE])
        out_screen = self.outputScreen.get_screen(surface)
        font = pygame.font.SysFont("freesansserif", 50);
        font_surface = font.render(self.compliments.get(), 1, (255,255,255))
        #TODO randomize
        font_surface = pygame.transform.rotozoom(font_surface, random.randrange(-15,15) ,1.6)
        font_size = font_surface.get_rect().size
        out_size = out_screen.get_rect().size
        out_screen.blit(font_surface, ((out_size[0]-font_size[0]) / 2, (out_size[1]-font_size[1]) / 2))

    def previewAndSnap(self):
        cam = self.camera
        #Live Preview
        #self._print("Live Preview")
        generator = cam.generate_preview()
        self.previewer.preview(generator, 10)

        #Capture
        self.outputScreen.drawText("Capturing, Hold Very Still!")
        cam.focus()

        file_data = cam.capture()

        #Save
        #self._print("Saving Image")
        local_file = self.save(file_data)
        #Review

        #self._print("Review")
        self.previewer.review(local_file)
        self._addCompliment()
        self.previewer.preview(generator, 4,  self.outputScreen.get_screen(Surfaces.DOWN_RIGHT))

        self.outputScreen.clear()
        #self._print("DONE")

        return local_file

    def performActions(self, images):
        process_thread = threading.Thread(target=self.actions.combine_and_upload_to_event, args=[images, PhotoBooth.EVENT_NAME])
        process_thread.start()
        self.processes.append(process_thread)


    def _boothAction(self, count=4):
            #cam = models.PhotoBoothCamera()
        #cam = self.camera
        #self.__updateFocus()
        # Mirror up and to speed things up, less sounds from camera for usability
        #cam.mirror_up()

        images = [self._previewAndSnap() for _ in range(count)]

        #self.cam.mirror_down()

        #Actions with list of 4 photos
        if ONLINE:
            self.performActions(images)
        self._print("Actions Performed")
        self.outputScreen.clear()
        self._print("Press Button to begin taking pictures")

        pass

    def _previewAndSnap(self):
        #cam = self.camera
        #Live Preview
        def frame_gen():
            m1 = mockImage("pi_photobooth/tests/imgs/test.jpg")
            m2 = mockImage("pi_photobooth/tests/imgs/test1.png")
            while True:
                if int(time.time()) % 2 == 0:
                    yield m1
                else:
                    yield m2
        generator = frame_gen()

        #Preview
        self._print("Live Preview")
        time.sleep(.25)
        self.previewer.preview(generator, PhotoBooth.LIVE_PREVIEW_SECONDS)
        #Capture
        self._print("Capture")
        time.sleep(.25)

        #Save
        self._print("Save Image")
        time.sleep(.25)

        #Review
        self._print("Review")
        time.sleep(.25)
        self.previewer.review(mockImage("pi_photobooth/tests/imgs/test1.png").filename)
        self._addCompliment()
        self.previewer.preview(generator, PhotoBooth.REVIEW_SECONDS,  self.outputScreen.get_screen(Surfaces.DOWN_RIGHT))

        #Review
        self._print("DONE")

        return "pi_photobooth/tests/imgs/test.jpg"

BtnPin = 12

if __name__ == "__main__":
    booth = PhotoBooth()
    booth.init()
    booth.run()