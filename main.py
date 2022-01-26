import pygame
import sys

from states.intro import Intro
from states.menu import Menu
from states.game import Game
from states.levels import Levels
from states.transition import Transition

class Main(object):
    def __init__(self):
        pygame.init()

        self.SCREEN_W = 920
        self.SCREEN_H = 640
        self.SCREEN_C = (int(self.SCREEN_W / 2), int(self.SCREEN_H / 2))
        self.SCREEN = pygame.display.set_mode((self.SCREEN_W, self.SCREEN_H))
        self.CLOCK = pygame.time.Clock()
        self.FONT = pygame.font.Font("assets/fonts/font.ttf", 25)

        self.DISPLAY = pygame.Surface((self.SCREEN_W, self.SCREEN_H), flags=pygame.SRCALPHA)

        pygame.display.set_caption("Floppy Sticks")
        pygame.display.set_icon(pygame.image.load("assets/images/icon.png"))

        self.sounds = {
            "click": pygame.mixer.Sound("assets/sounds/click.wav")}
        self.images = {
            "restart_button": pygame.image.load("assets/images/restart_button.png"),
            "compass_button": pygame.image.load("assets/images/compass_button.png")}

        self._events = {}

        self._states = {
            "intro": Intro(self),
            "menu": Menu(self),
            "game": Game(self),
            "levels": Levels(self),
            "transition": Transition(self)}
        self._state = "intro"

    def events(self):
        self._events.clear()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.shutdown()
            if event.type == pygame.MOUSEBUTTONDOWN:
                self._events["mousebuttondown"] = event
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    self._events["keydown-r"] = True
                if event.key == pygame.K_SPACE:
                    self._events["keydown-space"] = True
                if event.key == pygame.K_ESCAPE:
                    self._events["keydown-escape"] = True
        self._events["mouse_pos"] = pygame.mouse.get_pos()

    def update(self):
        self._states[self._state].update(self._events)
        self._states["transition"].update(self._events)

    def render(self):
        self.DISPLAY.fill((10, 20, 30, 50))

        # pygame.draw.line(self.DISPLAY, (255, 0, 0), (self.SCREEN_C[0], 0), (self.SCREEN_C[0], self.SCREEN_H))

        self._states[self._state].render(self.DISPLAY)
        self._states["transition"].render(self.DISPLAY)

        # self.render_text(self.DISPLAY, "fps " + str(round(self.CLOCK.get_fps(), 2)), 10, 10, False, False)

        self.SCREEN.blit(self.DISPLAY, (0, 0))

        pygame.display.update()

    def loop(self):
        while True:
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

    def shutdown(self):
        pygame.quit()
        sys.exit()

if __name__ == "__main__":
    Main().loop()
