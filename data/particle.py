import pygame
import random

class Particle(object):
    def __init__(self, x, y, radius, color):
        self.x = x
        self.y = y
        self.radius = radius
        self.color = color
        self.velx = random.uniform(-2.0, 2.0)
        self.vely = random.uniform(-2.0, 2.0)

    def update(self):
        self.x += self.velx
        self.y += self.vely
        self.color.a -= 5
        self.vely += 0.1

    def render(self, surface):
        pygame.draw.circle(surface, self.color, (self.x, self.y), self.radius)

    @staticmethod
    def update_particles(array):
        for particle in array:
            particle.update()

    @staticmethod
    def render_particles(array, surface):
        for i, particle in sorted(enumerate(array), reverse=True):
            particle.render(surface)
            if particle.color.a <= 0:
                array.pop(i)

    @staticmethod
    def spawn(x, y, amount=30):
        return [Particle(x, y, random.uniform(1, 3), pygame.Color(255, 0, 100)) for _ in range(amount)]
