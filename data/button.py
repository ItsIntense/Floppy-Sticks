import pygame

from math import dist

class Button(object):
    def __init__(self, x, y, image):
        self.x = x
        self.y = y
        self.image = image

    def render(self, surface):
        surface.blit(self.image, (self.x, self.y))

    def collide(self, position):
        return self.image.get_rect(topleft=(self.x, self.y)).collidepoint(position)
