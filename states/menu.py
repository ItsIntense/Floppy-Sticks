from states.state import State
from data.point import Point
from data.particle import Particle

class Menu(State):
    def __init__(self, manager):
        super().__init__(manager)

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
                    self.manager.sounds["click"].play()
                    if point.state == "static":
                        self.particles.extend(Particle.spawn(point.x, point.y))
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

        Particle.update_particles(self.particles)

        for i, point in enumerate(self.points):
            point.update()
            if point.state == "dynamic":
                if point.y > self.manager.SCREEN_H:
                    self.manager.transition_to("game" if i == 0 else "levels")

    def render(self, surface):
        Particle.render_particles(self.particles, surface)
        for point in self.points:
            point.render(surface)
        for label in self.lables:
            self.manager.render_text(surface, label[0], label[1], label[2], render_centerx=label[3])
