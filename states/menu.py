from states.state import State
from point import Point

from core_functions import spawn_particles

class Menu(State):
    def __init__(self, manager):
        super().__init__(manager)
        self.setup()

    def setup(self):
        self.points = [
            Point(self.manager.SCREEN_C[0], self.manager.SCREEN_C[1], "clickable"),
            Point(self.manager.SCREEN_C[0], self.manager.SCREEN_C[1] + 40, "clickable"),
            Point(self.manager.SCREEN_C[0], self.manager.SCREEN_C[1] + 80, "clickable"),
            Point(self.manager.SCREEN_C[0], self.manager.SCREEN_C[1] + 120, "clickable"),
            Point(self.manager.SCREEN_C[0] - 40, self.manager.SCREEN_C[1] + 80, "static"),
            Point(self.manager.SCREEN_C[0] - 40, self.manager.SCREEN_C[1] + 120, "static")]
        self.lables = [
            ("play", self.manager.SCREEN_C[0] + 30, self.manager.SCREEN_C[1], False),
            ("select level", self.manager.SCREEN_C[0] + 30, self.manager.SCREEN_C[1] + 40, False),
            ("music", self.manager.SCREEN_C[0] + 30, self.manager.SCREEN_C[1] + 80, False),
            ("sound", self.manager.SCREEN_C[0] + 30, self.manager.SCREEN_C[1] + 120, False)]
        self.particles = []

    def update(self, events):
        if events.get("mousebuttondown"):
            for i, point in enumerate(self.points):
                if point.is_over(events.get("mousebuttondown").pos):
                    if point.state == "static":
                        self.particles += spawn_particles(point.x, point.y)
                    match i:
                        case 0 | 1:
                            point.switch_state("dynamic")
                        case 2:
                            point.switch_state("static")
                            self.points[4].switch_state("clickable")
                        case 4:
                            point.switch_state("static")
                            self.points[2].switch_state("clickable")
                        case 3:
                            point.switch_state("static")
                            self.points[5].switch_state("clickable")
                        case 5:
                            point.switch_state("static")
                            self.points[3].switch_state("clickable")

        for i, point in enumerate(self.points):
            if point.state == "dynamic":
                if point.y > self.manager.SCREEN_H:
                    self.manager.transition_to("game" if i == 0 else "intro")
            point.update()

        for i, particle in sorted(enumerate(self.particles), reverse=True):
            particle.update()
            if particle.radius <= 0:
                self.particles.pop(i)

    def render(self, surface):
        for particle in self.particles:
            particle.render(surface)
        for point in self.points:
            point.render(surface)
        for label in self.lables:
            self.manager.render_text(surface, label[0], label[1], label[2], render_centerx=label[3])
