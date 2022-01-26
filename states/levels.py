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

    def update(self, events):
        if events.get("keydown-escape"):
            self.manager.transition_to("menu")
        if events.get("mousebuttondown"):
            for point in self.points:
                if point.is_over(events["mousebuttondown"].pos):
                    point.switch_state("dynamic")
                    self.manager.sounds["click"].play()

        for point in self.points:
            point.update()
            if point.y > self.manager.SCREEN_H:
                Utils.write_settings("level", self.points.index(point))
                self.manager.transition_to("game")

    def render(self, surface):
        for point in self.points:
            point.render(surface)
