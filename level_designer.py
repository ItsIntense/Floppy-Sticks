import pygame
import sys
import json

from data.softbody import SoftBody

class Main(object):
    def __init__(self):
        pygame.init()

        monitor_info = pygame.display.Info()
        self.SCREEN_W = round(monitor_info.current_w / 2)
        self.SCREEN_H = round(monitor_info.current_h / 1.7)
        self.SCREEN_C = (round(self.SCREEN_W / 2), round(self.SCREEN_H / 2))
        self.SCREEN = pygame.display.set_mode((self.SCREEN_W, self.SCREEN_H), flags=pygame.RESIZABLE)
        self.CLOCK = pygame.time.Clock()
        self.FONT = pygame.font.Font("assets/fonts/font.ttf", 25)

        self.DISPLAY = pygame.Surface((self.SCREEN_W, self.SCREEN_H), flags=pygame.SRCALPHA)

        pygame.display.set_caption("Level Designer")

        self.softbody = SoftBody()
        self.offset = [self.SCREEN_C[0], self.SCREEN_C[1] / 1.5]
        self.load_model("data\\title-model.json")
        self.holding = None
        self.dragging = None

    def load_model(self, path):
        with open(path, "r") as file:
            model = json.load(file)
        self.softbody.load_model(model, self.offset)

    def save_model(self, path):
        with open(path, "r") as file:
            model = json.load(file)
        model["points"].clear()
        model["sticks"].clear()
        model["static"].clear()
        model["dynamic"].clear()
        model["clickable"].clear()

    def events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.shutdown()
            if event.type == pygame.VIDEORESIZE:
                self.SCREEN_W = event.w
                self.SCREEN_H = event.h
                self.SCREEN_C = (round(self.SCREEN_W / 2), round(self.SCREEN_H / 2))
                self.SCREEN = pygame.display.set_mode((self.SCREEN_W, self.SCREEN_H), flags=pygame.RESIZABLE)
                self.DISPLAY = pygame.Surface((self.SCREEN_W, self.SCREEN_H), flags=pygame.SRCALPHA)
                self._states[self._state].setup()
                self._events["videoresize"] = True
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    for point in self.softbody.points:
                        if point.collide(event.pos):
                            self.holding = point
                            break
                    else:
                        self.softbody.add_point(event.pos[0], event.pos[1], "static")
                elif event.button == 3:
                    for point in self.softbody.points:
                        if point.collide(event.pos):
                            self.dragging = point

            if event.type == pygame.MOUSEBUTTONUP:
                self.holding = None
                self.dragging = None
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:
                    mouse_pos = pygame.mouse.get_pos()
                    for point in self.softbody.points:
                        if point.collide(mouse_pos):
                            point.switch_state("static")
                            break
                if event.key == pygame.K_2:
                    mouse_pos = pygame.mouse.get_pos()
                    for point in self.softbody.points:
                        if point.collide(mouse_pos):
                            point.switch_state("dynamic")
                            break
                if event.key == pygame.K_3:
                    mouse_pos = pygame.mouse.get_pos()
                    for point in self.softbody.points:
                        if point.collide(mouse_pos):
                            point.switch_state("clickable")
                            break
                if event.key == pygame.K_s:
                    self.save_model("data\\title-model.json")

    def update(self):
        self.softbody.update_points()
        self.softbody.update_sticks()

    def render(self):
        self.DISPLAY.fill((50, 50, 50))

        if self.holding:
            self.holding.x, self.holding.y = pygame.mouse.get_pos()

        if self.dragging:
            mouse_pos = pygame.mouse.get_pos()
            pygame.draw.aaline(self.DISPLAY, (255, 255, 255), (self.dragging.x, self.dragging.y), mouse_pos)
            for point in self.softbody.points:
                if point == self.dragging:
                    continue
                if point.collide(mouse_pos):
                    self.softbody.add_stick(self.dragging, point)
                    self.dragging = None
                    break

        self.softbody.render_sticks(self.DISPLAY)
        self.softbody.render_points(self.DISPLAY)

        self.render_text(self.DISPLAY, "Fps " + str(round(self.CLOCK.get_fps(), 2)), 10, 10, False, False)

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

    def shutdown(self):
        pygame.quit()
        sys.exit()

if __name__ == "__main__":
    Main().loop()
