from point import Point
from stick import Stick

from math import cos, sin, pi

class SoftBody:
    def __init__(self, gravity=0.25, friction=0.999):
        self.gravity = gravity
        self.friction = friction
        self.points = []
        self.sticks = []
        self.static = []
        self.dynamic = []
        self.clickable = []
    
    def load_model(self, model, offset):
        self.points.clear()
        self.sticks.clear()
        self.static.clear()
        self.dynamic.clear()
        self.clickable.clear()

        for i, angle, length, state in model["points"]:
            try:
                x = self.points[i].x
                y = self.points[i].y
            except IndexError:
                x, y = offset

            x += round(cos(-angle * pi / 180) * length)
            y += round(sin(-angle * pi / 180) * length)

            self.add_point(x, y, state)

        for stick in model["sticks"]:
            self.add_stick(self.points[stick[0]], self.points[stick[1]])

        self.static = [self.points[i] for i in model["static"]]
        self.dynamic = [self.points[i] for i in model["dynamic"]]
        self.clickable = [self.points[i] for i in model["clickable"]]

    def add_point(self, x, y, state):
        self.points.append(Point(x, y, state, gravity=self.gravity, friction=self.friction))

    def add_stick(self, point1, point2):
        self.sticks.append(Stick(point1, point2))

    def update_points(self):
        for point in self.points:
            point.update()

    def update_sticks(self):
        for stick in self.sticks:
            stick.update()

    def render_points(self, surface):
        for point in self.points:
            point.render(surface)

    def render_sticks(self, surface):
        for stick in self.sticks:
            stick.render(surface)
