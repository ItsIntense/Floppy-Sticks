import pygame

from random import uniform

class Particle:
    def __init__(self, x, y, radius):
        self.x = x
        self.y = y
        self.radius = radius
        self.speedx = round(uniform(-3.0, 3.0), 2)
        self.speedy = round(uniform(-3.0, 3.0), 2)

    def update(self):
        self.x += self.speedx
        self.y += self.speedy
        self.radius -= 0.1
        self.speedy += 0.1

    def render(self, surface):
        pygame.draw.circle(surface, (255, 0, 0), (self.x, self.y), self.radius)

        radius = self.radius * 2
        image = pygame.Surface((radius * 2, radius * 2))
        image.set_colorkey((0, 0, 0))
        pygame.draw.circle(image, (255, 0, 100), (radius, radius), radius)

        surface.blit(image, (self.x - radius, self.y - radius), special_flags=pygame.BLEND_RGB_ADD)
