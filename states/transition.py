from pygame import Surface, SRCALPHA
from states.state import State

class Transition(State):
    def __init__(self, manager):
        super().__init__(manager)

    def setup(self):
        self.image = Surface((self.manager.SCREEN_W, self.manager.SCREEN_H), flags=SRCALPHA)
        self.alpha = 0
        self.speed = 2
        self.active = False
        self.endstate = None

    def update(self, events, **kwargs):
        if self.active:
            self.image.fill((50, 50, 50, self.alpha))

    def render(self, surface):
        if self.active:
            surface.blit(self.image, (0, 0))
            self.alpha += self.speed
            if self.alpha >= 250:
                self.speed = -5
                self.manager._state = self.endstate
            elif self.alpha <= 0:
                self.setup()
