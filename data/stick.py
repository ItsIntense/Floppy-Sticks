import pygame

from math import dist, sqrt

class Stick:
    def __init__(self, point1, point2):
        self.point1 = point1
        self.point2 = point2
        self.length = dist((point1.x, point1.y), (point2.x, point2.y))

    def update(self):
        distx = self.point1.x - self.point2.x
        disty = self.point1.y - self.point2.y

        distance = sqrt(distx ** 2 + disty ** 2)
        difference = self.length - distance

        try:
            percent = difference / distance / 2
        except ZeroDivisionError:
            percent = 0

        offsetx = distx * percent
        offsety = disty * percent

        if self.point1.state == "dynamic":
            self.point1.x += offsetx
            self.point1.y += offsety
        if self.point2.state == "dynamic":
            self.point2.x -= offsetx
            self.point2.y -= offsety

    def render(self, surface):
        pygame.draw.aaline(surface, (255, 255, 255), (self.point1.x, self.point1.y), (self.point2.x, self.point2.y))
