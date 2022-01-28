import pygame

from math import dist

class Point(object):
    def __init__(self, x, y, state, gravity=0.3, friction=0.999):
        self.x = x
        self.y = y
        self.lastx = x
        self.lasty = y
        self.state = state
        self.gravity = gravity
        self.friction = friction
        self.load_image()

    def switch_state(self, state):
        self.state = state
        self.load_image()

    def load_image(self):
        self.image = pygame.image.load("assets/images/" + self.state + ".png")

    def update(self):
        if self.state == "dynamic": 
            velx = (self.x - self.lastx) * self.friction
            vely = (self.y - self.lasty) * self.friction

            self.lastx = self.x
            self.lasty = self.y

            self.x += velx
            self.y += vely
            self.y += self.gravity

    def render(self, surface):
        surface.blit(self.image, (self.x - 10, self.y - 10))

    def collide(self, position):
        return dist(position, (self.x, self.y)) < 10

    def collide_points(self, points):
        collisions = []
        for point in points:
            if dist((self.x, self.y), (point.x, point.y)) < 10:
                collisions.append(point)
        return collisions
