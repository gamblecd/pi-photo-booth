import models
import pygame
import gphoto2 as gp
import preview as pv
from outputs import OutputScreen, Surfaces
from inputs import Button
from enum import Enum
import os
import time
import threading
from background import actions
import random
import sys, select

import Queue

ONLINE = True
MOCK = False

class ThreadEvents(Enum):
    SHUTDOWN = "shutdown"
    SHOOTING = "photoshoot"

class mockImage():

    def __init__(self, filename):
        self.filename=filename

    def get_data_and_size(self):
        f = open(self.filename,'rb');
        return f.read()

class Compliments:
    def __init__(self):
        self.compliments = ["Your smile is contagious!",
                            "I like your style!",
                            "On a scale from 1 to 10, you're an 11",
                            "Beautiful!",
                            "Did you say cheese?",
                            "That color is perfect on you",
                            "Your hair looks stunning",
                            "You have the best ideas!",
                            "You're more fun than bubble wrap!",
                            "Gorgeous!",
                            "Look at these peeps!",
                            "Rockin' it!",
                            "Merry Christmas!",
                            "Hello, good looking!",
                            "Eh, try again on the next one?",
                            "You get an A+!",
                            "Do that again!",
                            "Oh, I can keep going",
                            "Well played.",
                            "You look so perfect."]

    def get(self):
        return random.choice(self.compliments)

class PhotoBooth:
    LIVE_PREVIEW_SECONDS = 10
    REVIEW_SECONDS = 4
    FRAME_COUNT = 4
    EVENT_NAME = "Christmas Party"

    def __initActions(self):
        print("loading Actions")
        if ONLINE:
            self.actions = actions.Actions()
        self.processes = []
        print("loading: Actions -- Complete")

    def __initScreen(self):
        pygame.init()
        self.screen = pygame.display.set_mode([1920, 1200], pygame.FULLSCREEN)
        pygame.display.update()
        self.outputScreen = OutputScreen(self.screen)

    def __initPreviewer(self):
        print("loading Previewer")
        self.previewer = pv.Previewer(self.screen)
        print("loading: Previewer -- Complete")

    def __initCamera(self):
        print("loading: Camera")
        self.context = gp.Context()
        self._camera = models.PhotoBoothCamera(self.context)
        if not MOCK:
            self._camera.init()
            print("loading: Camera -- Complete")
        else:
            self._camera.init()
            print("loading: Camera -- Mock -- Complete")



    def __loadMessageAsync(self, load_event):
        x = 0
        while not load_event.is_set():
            self.outputScreen.drawText("Loading" + ("." * x), erase=True)
            x += 1
        time.sleep(.1)
        self.outputScreen.drawText("Done!", erase=True)
        time.sleep(.25)

    def __loadMessage(self, load_event):
        loadMessageThread = threading.Thread(target=self.__loadMessageAsync, args=[load_event])
        loadMessageThread.start()
        return loadMessageThread

    @property
    def camera(self):
        if not self._camera.initiated:
            # Offline Camera
            return {}
        return self._camera

    def __init__(self):
        self.init_complete = False
        pass

    def init(self):
        self.__initScreen()
        load_event = threading.Event()
        messageThread = self.__loadMessage(load_event)
        try:
            self.acting = False
            self._button = Button()
            self.__initActions()
            self.__initPreviewer()
            self.__initCamera()
            self.compliments = Compliments()
            time.sleep(.1)
            self.init_complete = True
        except Exception as e:
            load_event.set()
            messageThread.join()
            print(e)
            self.outputScreen.drawText("Load Failure: {}".format(e.message), erase=True)
            self.init_complete = False
        load_event.set()
        messageThread.join()

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

    def save(self, file_data, folderName = EVENT_NAME):
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

    def keyboard_listener(self, queue, halt_event):
        while not halt_event.is_set():
            sys.stdin.flush()
            print("Waiting For Input")
            print("Press Enter, or Any Button to quit exit for quit.\n")
            # Slower spin loop on keyboard input
            loop, text = self.__wait_for_input(10)
            while loop and not halt_event.is_set():
                loop, text = self.__wait_for_input(10)
            if not queue.full():
                try:

                    if not text is None and len(text) > 0:
                        queue.put(ThreadEvents.SHUTDOWN)
                    else:
                        queue.put(ThreadEvents.SHOOTING)
                except Queue.Full:
                    print("Ignored input, keyboard")
            else:
                print("Ignored input, keyboard")

    def __wait_for_input(self, timeout=5):
        i, o, e = select.select([sys.stdin],[],[], timeout)
        if (i):
            return False, sys.stdin.readline().strip()
        else:
            return True, None

    def __show_main_screen(self):
        cam = self.camera
        self._print("Press Button to begin taking pictures", erase=True)
        battery_level = cam.get_config().get("batterylevel").value()
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
        queue = Queue.Queue(maxsize=1)

        halt_event = threading.Event()

        self._button.listen(self.buttonListener(queue, halt_event))

        keyboard_thread = threading.Thread(target=self.keyboard_listener, args=[queue, halt_event])
        keyboard_thread.start()
        self.processes.append(keyboard_thread)

        self.__start_shoot_set(queue, halt_event)

    def photo_shoot(self, count=FRAME_COUNT):
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

    # def previewAndSnap(self):
    #     cam = self.camera
    #     #Live Preview
    #     #self._print("Live Preview")
    #     generator = cam.generate_preview()
    #     self.previewer.preview(generator, PhotoBooth.LIVE_PREVIEW_SECONDS)

    #     #Capture
    #     self.outputScreen.drawText("Capturing, Hold Very Still!")
    #     cam.focus()

    #     file_data = cam.capture()

    #     #Save
    #     #self._print("Saving Image")
    #     local_file = self.save(file_data)
    #     #Review

    #     #self._print("Review")
    #     self.previewer.review(local_file)
    #     self._addCompliment()
    #     self.previewer.preview(generator, PhotoBooth.REVIEW_SECONDS,  self.outputScreen.get_screen(Surfaces.DOWN_RIGHT))

    #     self.outputScreen.clear()
    #     #self._print("DONE")

    #     return local_file

    def performActions(self, images):
        process_thread = threading.Thread(target=self.actions.combine_and_upload_to_event, args=[images, PhotoBooth.EVENT_NAME])
        process_thread.start()
        self.processes.append(process_thread)


    def _boothAction(self, count=FRAME_COUNT):
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

    def previewAndSnap(self):
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


if __name__ == "__main__":
    booth = PhotoBooth()
    booth.init()
    booth.run()
    #b = Button()
    #b.loop()
