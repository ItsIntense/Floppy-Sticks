from states.state import State
from data.softbody import SoftBody
from data.button import Button
from data.particle import Particle
from data.utils import Utils

class Game(State):
    def __init__(self, manager):
        super().__init__(manager)

    def setup(self):
        self.softbody = SoftBody()
        self.levels = Utils.read_models("models")
        self.level = Utils.read_settings(key="level")
        self.load_level(self.level)
        self.particles = []

        self.buttons = {
            "compass": Button(10, 10, self.manager.images["compass_button"]),
            "restart": Button(10, self.manager.SCREEN_H - 42, self.manager.images["restart_button"])}

        self.next = False
        self.restart = False

    def next_level(self):
        self.level += 1
        if self.level >= len(self.levels):
            self.level = 0
        self.softbody.load_model(self.levels[self.level], (self.manager.SCREEN_C[0], 250))

    def load_level(self, level):
        self.softbody.load_model(self.levels[level], (self.manager.SCREEN_C[0], 250))

    def restart_level(self):
        self.softbody.load_model(self.levels[self.level], (self.manager.SCREEN_C[0], 250))

    def update(self, events):
        if events.get("mousebuttondown"):
            for point in self.softbody.clickable:
                if point.is_over(events["mousebuttondown"].pos):
                    point.switch_state("dynamic")
                    self.manager.sounds["click"].play()
            for name, button in self.buttons.items():
                if button.is_over(events["mousebuttondown"].pos):
                    match name:
                        case "compass":
                            self.manager.transition_to("menu")
                            self.manager.sounds["click"].play()
                        case "restart":
                            self.restart = True
                            self.manager.sounds["click"].play()

        if events.get("keydown-escape"):
            self.manager.transition_to("menu")

        for button in self.buttons.values():
            if button.is_over(events["mouse_pos"]):
                button.image.set_alpha(100)
            else:
                button.image.set_alpha(255)

        Particle.update_particles(self.particles)

        self.softbody.update_points()
        for _ in range(2):
            self.softbody.update_sticks()

        for point in self.softbody.dynamic:
            collisions = point.collide_list(self.softbody.static)
            for collision in collisions:
                self.particles.extend(Particle.spawn(point.x, point.y, amount=50))
                collision.switch_state("dynamic")

        for point in self.softbody.dynamic:
            collisions = point.collide_list(self.softbody.clickable)
            for collision in collisions:
                collision.switch_state("dynamic")

        if len(self.softbody.points) == len(self.softbody.dynamic):
            self.next = True
        elif len(self.softbody.static) > 0 and len(self.softbody.clickable) == 0:
            self.restart = True

        if self.next:
            self.manager.transition_to("game", setup=False)
            if self.manager._states["transition"].alpha >= 250:
                self.next_level()
                self.next = False

        elif self.restart:
            self.manager.transition_to("game", setup=False)
            if self.manager._states["transition"].alpha >= 250:
                self.restart_level()
                self.restart = False

    def render(self, surface):
        Particle.render_particles(self.particles, surface)

        self.softbody.render_sticks(surface)
        self.softbody.render_points(surface)

        for button in self.buttons.values():
            button.render(surface)

        self.manager.render_text(surface, f"{self.level}/{len(self.levels) - 1}", self.manager.SCREEN_W - 40, 30)
