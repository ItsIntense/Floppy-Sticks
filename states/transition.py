import pygame

from states.state import State

class Transition(State):
    def __init__(self, manager):
        super().__init__(manager)
        self.setup()

    def setup(self):
        self.image = pygame.Surface((self.manager.SCREEN_W, self.manager.SCREEN_H))
        self.image.fill((10, 20, 30))
        self.image.set_alpha(0)
        self.alpha = 0
        self.speed = 2
        self.active = False
        self.endstate = None

    def update(self, events):
        if self.active:
            self.alpha += self.speed
            self.image.set_alpha(self.alpha)
            if self.alpha >= 250:
                self.speed = -5
                self.manager._state = self.endstate
            elif self.alpha <= 0:
                self.setup()

    def render(self, surface):
        if self.active:
            surface.blit(self.image, (0, 0))
