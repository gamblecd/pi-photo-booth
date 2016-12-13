from __future__ import print_function

import pygame
import io

from PIL import Image

import time
import gphoto2 as gp

'''
Handles Previews for a camera, shows a preview and a review after the image
was taken.
'''


class Previewer:

    def __init__(self, screen):
        self.screen = screen

    def previewFrame(self, camera):
        pass

    def livePreview(self, camera, seconds):
        pass

    def _displayLiveFrame(self, image):
        mode = image.mode
        size = image.size
        data = image.tobytes()
        frame = pygame.image.frombuffer(data, size, mode)
        self.screen.blit(frame, (0, 0))
        pygame.display.update()

    def preview(self, camera, seconds=6):
        t_end = time.time() + seconds

        #For however long we want to
        while t_end > time.time():
            # Grab Preview
            camera_file = camera.capture_preview()
            file_data = camera_file.get_data_and_size()

            # display image
            image = Image.open(io.BytesIO(file_data))
            self._displayLiveFrame(image)
        return 0

    def review(self, camera, seconds):
        pass


