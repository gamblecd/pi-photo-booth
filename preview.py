from __future__ import print_function

import pygame
import io

from PIL import Image

import time

def count_helper(seconds, init_val, countFn):
    start = int(time.time())
    now = int(time.time())
    val = init_val;
    count = 0;
    yield val
    while not count == seconds:
        if not (now - start) == count:
            val = countFn(now, start)
            count +=1
        yield val
        now = int(time.time())


def count_up(seconds):
    return count_helper(seconds, 0, lambda x, y: (x-y))

def count_down(seconds):
    return count_helper(seconds, seconds, lambda x, y: seconds - (x-y))
   


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

    def producer(self, frame_generator):
        # Grab Preview
        while True:
            camera_file = next(frame_generator())
            file_data = camera_file.get_data_and_size()
            # display image
            image = Image.open(io.BytesIO(file_data))
            yield image
        
    def test_producer(self, camera, seconds):
        t_end = time.time() + seconds
        while t_end > time.time():
            yield Image.open(io.FileIO("test/test1.jpeg"))

    def _displayLive(self, image, on_screen=None):
        if not on_screen:
            on_screen = self.screen
        mode = image.mode
        size = image.size
        data = image.tobytes()
        frame = pygame.image.frombuffer(data, size, mode)
        frame = pygame.transform.scale(frame, on_screen.get_rect().size)
        screen.blit(frame, (0, 0))
    
    def _displayCountdown(self, generator):
        screen = self.screen
        #Clears text
        font = pygame.font.SysFont("freesansserif", 30);
        screen.blit(font.render(str(next(generator)), 1, (0,0,0)), screen.get_rect());

    def preview(self, camera, seconds=6, on_screen=None, show_timer=True):
        if not on_screen:
            on_screen = self.screen
        #For however long we want to
        generator = count_down(seconds)
        for img in self.test_producer(camera, seconds):
            self._displayLive(img, on_screen)
            if show_timer:
                try:
                    self._displayCountdown(generator)
                except StopIteration:
                    #ran out of generator values
                    pass
    
            pygame.display.update();
        return 0

    def review(self, screen, img, seconds):
        pass

if __name__ == "__main__":
    pygame.init()
    screen = pygame.display.set_mode([300, 100])
    pygame.display.update()
    Previewer(screen).preview(None, 4)
    