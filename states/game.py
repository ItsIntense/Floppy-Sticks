from states.state import State
from softbody import SoftBody
from core_functions import read_models, spawn_particles

class Game(State):
    def __init__(self, manager):
        super().__init__(manager)
        self.setup()

    def setup(self):
        self.softbody = SoftBody()
        self.levels = read_models ("models")
        self.level = -1
        self.next_level()
        self.particles = []

    def next_level(self):
        self.level += 1
        if self.level >= len(self.levels):
            self.level = 0
        self.softbody.load_model(self.levels[self.level], (self.manager.SCREEN_C[0], 200))

    def load_level(self, level):
        self.softbody.load_model(self.levels[level], (self.manager.SCREEN_C[0], 200))

    def restart_level(self):
        self.softbody.load_model(self.levels[self.level], (self.manager.SCREEN_C[0], 200))

    def update(self, events):
        if events.get("mousebuttondown"):
            for point in self.softbody.clickable:
                if point.is_over(events["mousebuttondown"].pos):
                    point.switch_state("dynamic")
                    self.softbody.dynamic.append(point)
                    self.softbody.clickable.remove(point)
        if events.get("keydown-escape"):
            self.manager.transition_to("menu")
        if events.get("keydown-r"):
            self.read_models("models")
            self.restart_level()

        self.softbody.update_points()
        for i in range(5):
            self.softbody.update_sticks()

        for point in self.softbody.dynamic:
            collisions = point.collide_list(self.softbody.static)
            for collision in collisions:
                self.particles += spawn_particles(point.x, point.y)
                collision.switch_state("dynamic")
                self.softbody.dynamic.append(collision)
                self.softbody.static.remove(collision)

        for point in self.softbody.dynamic:
            collisions = point.collide_list(self.softbody.clickable)
            for collision in collisions:
                collision.switch_state("dynamic")
                self.softbody.dynamic.append(collision)
                self.softbody.clickable.remove(collision)

        if len(self.softbody.points) == len(self.softbody.dynamic):
            self.manager.transition_to("game", setup=False)
            if self.manager._states["transition"].alpha >= 250:
                self.next_level()

        elif len(self.softbody.static) > 0 and len(self.softbody.clickable) == 0:
            self.manager.transition_to("game", setup=False)
            if self.manager._states["transition"].alpha >= 250:
                self.restart_level()
        
        for i, particle in sorted(enumerate(self.particles), reverse=True):
            particle.update()
            if particle.radius <= 0:
                self.particles.pop(i)

    def render(self, surface):
        for particle in self.particles:
            particle.render(surface)
        self.softbody.render_sticks(surface)
        self.softbody.render_points(surface)
