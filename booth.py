import models
import pygame
import gphoto2 as gp
import preview as pv
from outputs import OutputScreen, Surfaces
import os
import time
import threading
from background import actions
ONLINE = False

class mockImage():
    
    def __init__(self, filename):
        self.filename=filename

    def get_data_and_size(self):
        f = open(self.filename,'rb');
        return f.read()


class PhotoBooth:
    LIVE_PREVIEW_SECONDS = 8
    REVIEW_SECONDS = 2
    FRAME_COUNT = 4
    EVENT_NAME = "TestEventForUpload"

    def __initActions(self):
        print("Loading Actions")
        if ONLINE:
            self.actions = actions.Actions();
        self.processes = []

    def __initScreen(self):
        pygame.init()
        self.screen = pygame.display.set_mode([1200, 800])
        pygame.display.update()
        self.outputScreen = OutputScreen(self.screen)

    def __initPreviewer(self):
        self.previewer = pv.Previewer(self.screen)

    def __initCamera(self):
        self.context = gp.Context()
        self.camera = models.PhotoBoothCamera(self.context)

    def __loadMessageAsync(self):
        x = 0
        while not self.loaded:
            self.outputScreen.drawText("Loading" + ("." * x))
            x += 1
        time.sleep(.1)
        self.outputScreen.drawText("Done!")
        time.sleep(.25)

    def __loadMessage(self):
        loadMessageThread = threading.Thread(target=self.__loadMessageAsync)
        loadMessageThread.start()
        return loadMessageThread

    def __init__(self):
        self.loaded = False
        self.__initScreen()
        messageThread = self.__loadMessage();
        self.__initActions()
        print("loading Previewer")
        self.__initPreviewer()
        print("loading Camera")
        #self.__initCamera()
        time.sleep(.1)
        self.loaded = True;
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
        img.save(imglocation)

    def waitForInput(self):
        return raw_input("Press Enter, or Any Button to quit exit for quit.\n")

    def run(self):
        print("Display Instruction Screen")
        exit = False
        while not exit:
            print("Waiting For Input")
            self._print("Press Button to begin taking pictures")

            text = raw_input("Press Enter, or Any Button to quit exit for quit.\n")
            if len(text) > 0:
                exit = True
            else:
                self._boothAction()
   
    def photo_shoot(self, count=FRAME_COUNT):
        #cam = models.PhotoBoothCamera()
        cam = self.camera
        self.__updateFocus()
        # Mirror up and to speed things up, less sounds from camera for usability
        cam.mirror_up()

        images = [self.previewAndSnap() for _ in range(count)]
        
        cam.mirror_down()

        #Actions with list of 4 photos
        self.performActions(images)
        pass

    def _print(self, message):
        self.outputScreen.drawText(message)

    def previewAndSnap(self):
        cam = self.camera
        #Live Preview
        generator = cam.generate_preview()
        self.previewer.preview(generator, PhotoBooth.LIVE_PREVIEW_SECONDS)
        #Capture
        file_data = cam.capture()
        #Save
        local_file = self.save(file_data)
        #Review
        self.previewer.review(local_file)
        self.previewer.preview(generator, PhotoBooth.REVIEW_SECONDS,  self.outputScreen.get_screen(Surfaces.DOWN_RIGHT))
        self._print("DONE")

        return local_file

    def performActions(self, images):
        process_thread = threading.Thread(target=self.actions.combineAndUploadToEvent, args=[images, PhotoBooth.EVENT_NAME])
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
        self._print("ActionsPerformed")
        pass
   


    def _previewAndSnap(self):
        #cam = self.camera
        #Live Preview
        def frame_gen():
            m1 = mockImage("test/test1.jpeg")
            m2 = mockImage("test/test1.png")
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
        self.previewer.review(mockImage("test/test1.png").filename)
        self.previewer.preview(generator, PhotoBooth.REVIEW_SECONDS,  self.outputScreen.get_screen(Surfaces.DOWN_RIGHT))
        
        
        
        #Review
        self._print("DONE")

        return "test/test1.jpeg"


if __name__ == "__main__":
    booth = PhotoBooth()
    booth.run();