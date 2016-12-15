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

    def producer(self, frame_generator, seconds):
        # Grab Preview
        t_end = time.time() + seconds
        camera_file = next(frame_generator)
        while t_end > time.time():
            file_data = camera_file.get_data_and_size()
            # display image
            image = Image.open(io.BytesIO(file_data))
            yield image
            camera_file = next(frame_generator)
        

    def _displayFrame(self, image, on_screen=None):
        if not on_screen:
            on_screen = self.screen
        mode = image.mode
        size = image.size
        data = image.tobytes()
        frame = pygame.image.frombuffer(data, size, mode)
        frame = pygame.transform.scale(frame, on_screen.get_rect().size)
        on_screen.blit(frame, (0, 0))

    def _displayCountdown(self, generator, on_screen):
        #Clears text
        font = pygame.font.SysFont("freesansserif", 30);
        on_screen.blit(font.render(str(next(generator)), 1, (0,0,0)), on_screen.get_rect());

    def preview(self, frame_generator, seconds=6, on_screen=None, show_timer=True):
        if not on_screen:
            on_screen = self.screen
        #For however long we want to
        generator = count_down(seconds)
        for img in self.producer(frame_generator, seconds):
            self._displayFrame(img, on_screen)
            if show_timer:
                try:
                    self._displayCountdown(generator, on_screen)
                except StopIteration:
                    #ran out of generator values
                    pass
            pygame.display.update()
        return 0

    def review(self, img, on_screen=None):
        if not on_screen:
            on_screen = self.screen
        self._displayFrame(Image.open(img), on_screen)
        pygame.display.update()


class mockImage():
    
    def __init__(self, filename):
        self.filename=filename

    def get_data_and_size(self):
        f = open(self.filename,'rb');
        return f.read()


if __name__ == "__main__":
    from outputs import OutputScreen
    pygame.init()
    screen = pygame.display.set_mode([1200, 800])
    pygame.display.update()
    screens = OutputScreen(screen)
    time.sleep(.5)
    
            
    def frame_gen():
        m1 = mockImage("test/test1.jpeg")
        m2 = mockImage("test/test1.png")
        while True:
            if int(time.time()) % 2 == 0:
                yield m1
            else:
                yield m2

    frame_g = frame_gen()
    Previewer(screen).preview(frame_g, 6, on_screen=screens.get_screen(6))
    #
    Previewer(screen).review("test/test1.png", on_screen=screens.get_screen(6))
    Previewer(screen).preview(frame_g, 2, on_screen=screens.get_screen(3), show_timer=False)
    
    Previewer(screen).preview(frame_g, 3, on_screen=screens.get_screen(6))
    