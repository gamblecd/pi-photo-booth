import models
import pygame
import gphoto2 as gp
import preview as pv
import outputs
import os
import time


class PhotoBooth:
    LIVE_PREVIEW_SECONDS = 8
    FRAME_COUNT = 4

    def __initScreen(self):
        pygame.init()
        self.screen = pygame.display.set_mode([0, 0], pygame.FULLSCREEN)
        pygame.display.update()
        self.outputScreen = outputs.OutputScreen(self.screen)

    def __initPreviewer(self):
        self.previewer = pv.Previewer(self.screen)

    def __initCamera(self):
        self.context = gp.Context()
        self.camera = models.PhotoBoothCamera(self.context)

    def __init__(self):
        self.__initScreen()
        self.__loadMessage()
        self.__initPreviewer()
        self.__initCamera()

    def __loadMessage(self):
        for x in range(30):
            self.outputScreen.drawText("Loading Text" + ("." * x))
            time.sleep(1. / 30)

    #set autofocus, take a frame, ignore picture
    def __updateFocus(self):
        cam = self.camera
        cam.focus()
        cam.capture()


    def save_picture(file_data, location):
        file_data.save(location)

    def save(self, file_data):
        cam = self.camera
        img = cam.get_image(file_data)
        imglocation = "{0}/{1}".format("folder1", file_data.name)
        print(imglocation)
        if not os.path.exists("folder1"):
            os.makedirs("folder1")
        img.save(imglocation)

    def runBooth(self, count=FRAME_COUNT):
        #cam = models.PhotoBoothCamera()
        cam = self.camera
        self.__updateFocus()
        # Mirror up and to speed things up, less sounds from camera for usability
        cam.mirror_up()

        images = [None * count]
        for x in range(count):
            images[x] = self._previewAndSnap()
        self.cam.mirror_down()

        #Actions with list of 4 photos
        pass

    def _previewAndSnap(self):
        cam = self.camera

        #Live Preview
        self.previewer.preview(cam, PhotoBooth.LIVE_PREVIEW_SECONDS)

        #Capture
        file_data = self.camera.capture()

        #Save And Review
        local_file = self.save(file_data)

        #Review
        self.previewer.review(local_file)
        print("DONE")

        return local_file
    def previewAndSnap(self):
        cam = self.camera

        #Live Preview
        self.previewer.preview(cam, PhotoBooth.LIVE_PREVIEW_SECONDS)

        #Capture
        file_data = self.camera.capture()

        #Save And Review
        local_file = self.save(file_data)

        #Review
        self.previewer.review(local_file)
        print("DONE")

        return local_file