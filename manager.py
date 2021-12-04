import pygame
import sys

from states.intro import Intro
from states.menu import Menu
from states.game import Game
from states.levels import Levels
from states.transition import Transition

class Manager:
    def __init__(self):
        pygame.init()

        self.SCREEN_W = 920
        self.SCREEN_H = 640
        self.SCREEN_C = (int(self.SCREEN_W / 2), int(self.SCREEN_H / 2))
        self.SCREEN = pygame.display.set_mode((self.SCREEN_W, self.SCREEN_H))
        self.CLOCK = pygame.time.Clock()
        self.FONT = pygame.font.Font("freesansbold.ttf", 20)

        pygame.display.set_caption("Dead Sticks")

        self._events = {}

        self._states = {
            "intro": Intro(self),
            "menu": Menu(self),
            "game": Game(self),
            "levels": Levels(self),
            "transition": Transition(self)}
        self._state = "intro"

    def events(self):
        self._events = {}
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                self._events["mousebuttondown"] = event
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    self._events["keydown-r"] = True
                if event.key == pygame.K_SPACE:
                    self._events["keydown-space"] = True
                if event.key == pygame.K_ESCAPE:
                    self._events["keydown-escape"] = True

    def update(self):
        self._states[self._state].update(self._events)
        self._states["transition"].update(self._events)

    def render(self):
        self.SCREEN.fill((10, 20, 30))

        self._states[self._state].render(self.SCREEN)
        self._states["transition"].render(self.SCREEN)

        # self.render_text(self.SCREEN, "fps " + str(round(self.CLOCK.get_fps(), 2)), 10, 10, False, False)

        pygame.display.update()

    def loop(self):
        self.events()
        self.update()
        self.render()
        self.CLOCK.tick(60)

    def render_text(self, surface, text, x, y, render_centerx=True, render_centery=True):
        for i, line in enumerate(text.split("\n")):
            text_surface = self.FONT.render(line, True, (255, 255, 255))
            match render_centerx, render_centery:
                case True, True:
                    text_rect = text_surface.get_rect(center=(x, y + text_surface.get_height() * i))
                case True, False:
                    text_rect = text_surface.get_rect(centerx=x, top=y + text_surface.get_height() * i)
                case False, True:
                    text_rect = text_surface.get_rect(left=x, centery=y + text_surface.get_height() * i)
                case False, False:
                    text_rect = text_surface.get_rect(topleft=(x, y + text_surface.get_height() * i))
            surface.blit(text_surface, text_rect)

    def transition_to(self, state, setup=True):
        if not self._states["transition"].active:
            if setup: self._states[state].setup()
            self._states["transition"].active = True
            self._states["transition"].endstate = state

if __name__ == "__main__":
    m = Manager()
    while True:
        m.loop()
