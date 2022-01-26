from states.state import State
from data.point import Point

class Intro(State):
    def __init__(self, manager):
        super().__init__(manager)

    def setup(self):
        self.point = Point(self.manager.SCREEN_C[0], self.manager.SCREEN_C[1], "clickable")

    def update(self, events):
        if events.get("mousebuttondown"):
            if self.point.is_over(events["mousebuttondown"].pos):
                self.point.switch_state("dynamic")
                self.manager.sounds["click"].play()

        self.point.update()
        if self.point.state == "dynamic":
            self.manager.transition_to("menu")

    def render(self, surface):
        self.manager.render_text(surface, "These types of circles\nare clickable", self.manager.SCREEN_C[0], self.manager.SCREEN_C[1] - 70)
        self.point.render(surface)
