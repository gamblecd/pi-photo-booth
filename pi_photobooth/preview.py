from __future__ import print_function

import pygame
import io

from PIL import Image

import time

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

    def _scale_size(self, orig_size, new_surface_size):
        ix, iy = orig_size
        bx, by = new_surface_size
        if ix > iy:
            #fit to width
            scale_factor = (bx / float(ix))
            sy = scale_factor * iy
            if sy > by:
                scale_factor = (by/float(iy))
                sx = scale_factor = ix
                sy = by
            else:
                sx = bx
        else:
            # fit to height
            scale_factor = (by / float(iy))
            sx = scale_factor * ix
            if sx > bx:
                scale_factor = (bx/float(ix))
                sx=bx
                sy=scale_factor * iy
            else:
                sy=by
        return (sx, sy)

    def _displayFrame(self, image, on_screen=None, centered=True):
        if not on_screen:
            on_screen = self.screen
        mode = image.mode
        size = image.size
        data = image.tobytes()
        frame = pygame.image.frombuffer(data, size, mode)
        #scale_size = self._scale_size(size, on_screen.get_rect().size)

        out_size = on_screen.get_rect().size
        frame = pygame.transform.scale(frame, out_size)
        on_screen.blit(frame, (0,0))

        #TODO scale
        #on_screen.blit(frame, ((out_size[0]-scale_size[0]) / 2, (out_size[1]-scale_size[1]) / 2))

    def _displayCountdown(self, generator, on_screen):
        #Clears text
        font = pygame.font.SysFont("freesansserif", 300);
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
        print(img)
        self._displayFrame(Image.open(img), on_screen)
        pygame.display.update()




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
