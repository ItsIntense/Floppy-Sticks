from states.state import State
from data.point import Point
from data.utils import Utils

class Levels(State):
    def __init__(self, manager):
        super().__init__(manager)

    def setup(self):
        self.points = []
        for y in range(60, 200, 60):
            for x in range(0, 310, 60):
                self.points.append(Point(x + 310, y, "clickable"))

    def update(self, events, **kwargs):
        if events.get("mousebuttondown"):
            for point in self.points:
                if point.collide(events["mousebuttondown"].pos):
                    point.switch_state("dynamic")
                    self.manager.sounds["click"].play()

        for point in self.points:
            point.update()
            if point.state == "dynamic":
                Utils.write_settings("level", self.points.index(point))
                self.manager.transition_to("game")

    def render(self, surface):
        for point in self.points:
            point.render(surface)
