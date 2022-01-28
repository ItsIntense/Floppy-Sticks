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

        self.MONITOR_SIZE = (pygame.display.Info().current_w, pygame.display.Info().current_h)
        self.SCREEN_W = round(self.MONITOR_SIZE[0] / 2)
        self.SCREEN_H = round(self.MONITOR_SIZE[1] / 1.7)
        self.SCREEN_C = (round(self.SCREEN_W / 2), round(self.SCREEN_H / 2))
        self.SCREEN = pygame.display.set_mode((self.SCREEN_W, self.SCREEN_H), flags=pygame.RESIZABLE)
        self.CLOCK = pygame.time.Clock()
        self.DISPLAY = pygame.Surface((self.SCREEN_W, self.SCREEN_H), flags=pygame.SRCALPHA)

        self.fullscreen = False

        pygame.display.set_caption("Floppy Sticks")
        pygame.display.set_icon(pygame.image.load("assets/images/icon.png"))
        # pygame.mouse.set_visible(False)

        self.fonts = {
            "general": pygame.font.Font("assets/fonts/oswald.ttf", 25),
            "title": pygame.font.Font("assets/fonts/pressstart2p.ttf", 35)}

        self.images = {
                    "restart_button": pygame.image.load("assets/images/restart_button.png"),
                    "compass_button": pygame.image.load("assets/images/compass_button.png")}

        self.sounds = {
            "click": pygame.mixer.Sound("assets/sounds/click.wav")}

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
                if event.button == 1:
                    self._events["mousebuttondown"] = event
            if event.type == pygame.VIDEORESIZE:
                if not self.fullscreen:
                    self.SCREEN_W = event.w
                    self.SCREEN_H = event.h
                    self.SCREEN_C = (round(self.SCREEN_W / 2), round(self.SCREEN_H / 2))
                    self.SCREEN = pygame.display.set_mode((self.SCREEN_W, self.SCREEN_H), flags=pygame.RESIZABLE)
                    self.DISPLAY = pygame.Surface((self.SCREEN_W, self.SCREEN_H), flags=pygame.SRCALPHA)
                    self._states[self._state].setup()
                    self._events["videoresize"] = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_F11:
                    self.fullscreen = not self.fullscreen
                    if self.fullscreen:
                        self.SCREEN_W = self.MONITOR_SIZE[0]
                        self.SCREEN_H = self.MONITOR_SIZE[1]
                        self.SCREEN = pygame.display.set_mode((self.SCREEN_W, self.SCREEN_H), flags=pygame.FULLSCREEN)
                    else:
                        self.SCREEN_W = round(self.MONITOR_SIZE[0] / 2)
                        self.SCREEN_H = round(self.MONITOR_SIZE[1] / 1.7)
                        self.SCREEN = pygame.display.set_mode((self.SCREEN_W, self.SCREEN_H), flags=pygame.RESIZABLE)
                    self.SCREEN_C = (round(self.SCREEN_W / 2), round(self.SCREEN_H / 2))
                    self.DISPLAY = pygame.Surface((self.SCREEN_W, self.SCREEN_H), flags=pygame.SRCALPHA)
                    self._states[self._state].setup()
                    self._events["keydown-F11"] = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_F11:
                    self.fullscreen = not self.fullscreen
                    if self.fullscreen:
                        self.SCREEN_W = self.MONITOR_SIZE[0]
                        self.SCREEN_H = self.MONITOR_SIZE[1]
                        self.SCREEN = pygame.display.set_mode((self.SCREEN_W, self.SCREEN_H), flags=pygame.FULLSCREEN)
                    else:
                        self.SCREEN_W = round(self.MONITOR_SIZE[0] / 2)
                        self.SCREEN_H = round(self.MONITOR_SIZE[1] / 1.7)
                        self.SCREEN = pygame.display.set_mode((self.SCREEN_W, self.SCREEN_H), flags=pygame.RESIZABLE)
                    self.SCREEN_C = (round(self.SCREEN_W / 2), round(self.SCREEN_H / 2))
                    self.DISPLAY = pygame.Surface((self.SCREEN_W, self.SCREEN_H), flags=pygame.SRCALPHA)
                    self._states[self._state].setup()
                    self._events["keydown-F11"] = True

    def update(self):
        self._states[self._state].update(self._events, mouse_pos=pygame.mouse.get_pos())
        self._states["transition"].update(self._events)

    def render(self):
        self.DISPLAY.fill((0, 0, 0, 50))

        # pygame.draw.line(self.DISPLAY, (255, 0, 0), (self.SCREEN_C[0], 0), (self.SCREEN_C[0], self.SCREEN_H))

        self._states[self._state].render(self.DISPLAY)
        self._states["transition"].render(self.DISPLAY)

        self.render_text(self.DISPLAY, "Fps " + str(round(self.CLOCK.get_fps(), 2)), 10, 10, render_centerx=False, render_centery=False)

        # pygame.draw.circle(self.DISPLAY, (255, 0, 130), pygame.mouse.get_pos(), 7)

        self.SCREEN.blit(self.DISPLAY, (0, 0))

        pygame.display.update()

    def loop(self):
        while True:
            self.events()
            self.update()
            self.render()
            self.CLOCK.tick(60)

    def render_text(self, surface, text, x, y, font="general", render_centerx=True, render_centery=True, overlay=True):
        for i, line in enumerate(text.split("\n")):
            text_surface = self.fonts[font].render(line, True, (255, 255, 255))
            match render_centerx, render_centery:
                case True, True:
                    text_rect = text_surface.get_rect(center=(x, y + text_surface.get_height() * i))
                case True, False:
                    text_rect = text_surface.get_rect(centerx=x, top=y + text_surface.get_height() * i)
                case False, True:
                    text_rect = text_surface.get_rect(left=x, centery=y + text_surface.get_height() * i)
                case False, False:
                    text_rect = text_surface.get_rect(topleft=(x, y + text_surface.get_height() * i))
            if overlay:
                text_surface_back = self.fonts[font].render(line, True, (100, 100, 100))
                text_rect_back = text_rect.copy()
                text_rect_back.x += 3
                text_rect_back.y += 3
                surface.blit(text_surface_back, text_rect_back)
            surface.blit(text_surface, text_rect)

    def transition_to(self, state, setup=True, speed=2):
        if not self._states["transition"].active:
            self._states["transition"].setup()
            self._states["transition"].speed = speed
            if setup: self._states[state].setup()
            self._states["transition"].active = True
            self._states["transition"].endstate = state

    def shutdown(self):
        pygame.quit()
        sys.exit()

if __name__ == "__main__":
    Main().loop()
