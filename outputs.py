import pygame
from enum import Enum
import time

white = pygame.Color(255, 255, 255)
black = pygame.Color(0, 0, 0)

class Surfaces(Enum):
    UP_LEFT = 0
    UP_RIGHT = 1
    DOWN_LEFT = 2
    DOWN_RIGHT = 3
    LIVE_PREVIEW = 3
    LEFT_SIDE = 4
    RIGHT_SIDE = 5
    FULLSCREEN = 6


class Positions:

    @classmethod
    def bottom_left(self, pW, pH, cW, cH):
        return (0, ((pH) - (cH)))

    @classmethod
    def centered(self, pW, pH, cW, cH):
        return ((pW / 2) - (cW / 2), ((pH / 2) - (cH / 2)))


class OutputScreen:

    def __init__(self, screen):
        self.screen = screen
        quadrants = [None] * 7
        w = screen.get_width()
        h = screen.get_height() 
        quadrant_size = (w / 2, h / 2)
        vertical_half_size = (w / 2, h)
        quadrants[0] = self.screen.subsurface(pygame.Rect((0, 0), quadrant_size))
        quadrants[1] = self.screen.subsurface(pygame.Rect((w / 2, 0), quadrant_size))
        quadrants[2] = self.screen.subsurface(pygame.Rect((0, h / 2), quadrant_size))
        quadrants[3] = self.screen.subsurface(pygame.Rect((w / 2, h / 2), quadrant_size))
        quadrants[4] = self.screen.subsurface(pygame.Rect((0, 0), vertical_half_size))
        quadrants[5] = self.screen.subsurface(pygame.Rect((w / 2, 0), vertical_half_size))
        quadrants[6] = self.screen.subsurface(pygame.Rect((0, 0), (w, h)))
        self.quadrants = quadrants

        self.identify()
    
    def get_screen(self, surface):
        return self.quadrants[surface.value]

    def identify(self):
        color = black
        for x in range(4):
            color = map(lambda x: x+60, color)
            color[3] = 255
            self.quadrants[x].fill(color)
        pygame.display.update();

    def drawText(self, message, location=Surfaces.DOWN_LEFT):
        screen = self.quadrants[location.value]
        text_width = 600
        text_height = 60
        surface_width = screen.get_width()
        surface_height = screen.get_height()
       
        #Clears text
        self.identify()
        font = pygame.font.SysFont("freesansserif", 30);
        screen.blit(font.render(message, 1, white), 
        screen.get_rect());
        pygame.display.update();

    def drawImage(self, image_data, surface=Surfaces.UP_LEFT):
        mode = image_data.mode
        size = image_data.size
        data = image_data.tobytes()
        frame = pygame.image.frombuffer(data, size, mode)
        self.screen.blit(frame, (0, 0))
        pygame.display.update()


if __name__ == "__main__":
    pygame.init()
    screen = pygame.display.set_mode([1200, 800])
    pygame.display.update()
    OutputScreen(screen)
    time.sleep(2)