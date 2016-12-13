import pygame
from enum import Enum

white = pygame.Color(255, 255, 255)
black = pygame.Color(0, 0, 0)

class Surfaces(Enum):
    UP_LEFT = 0
    UP_RIGHT = 1
    DOWN_LEFT = 2
    DOWN_RIGHT = 3
    LIVE_PREVIEW = 3
    FULLSCREEN = 4


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
        quadrants = []
        w = screen.width
        h = screen.height
        quadrants[0] = self.screen.subsurface(pygame.Rect(0, 0, w / 2, h / 2))
        quadrants[1] = self.screen.subsurface(pygame.Rect(w / 2, 0, w, h / 2))
        quadrants[2] = self.screen.subsurface(pygame.Rect(0, h / 2, w / 2, h))
        quadrants[3] = self.screen.subsurface(pygame.Rect(w / 2, h / 2, w, h))
        quadrants[4] = self.screen.subsurface(pygame.Rect(0, 0, w, h))
        self.quadrants

    def drawText(self, message, location=Positions.bottom_left):
        screen = self.screen
        text_width = 600
        text_height = 60
        surface_width = self.screen.get_width()
        surface_height = self.screen.get_height()
        centered = location(surface_width, surface_height,
                                         text_width, text_height)
        screen.blit(pygame.font.SysFont("freesansserif", 40, bold=1)
        .render(message, 1, white), (centered[0] + 10, centered[1] + 10));
        pygame.display.update();

    def drawImage(self, image_data, surface=Surfaces.UP_LEFT):
        mode = image_data.mode
        size = image_data.size
        data = image_data.tobytes()
        frame = pygame.image.frombuffer(data, size, mode)
        self.screen.blit(frame, (0, 0))
        pygame.display.update()
