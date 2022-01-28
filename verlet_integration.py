import pygame
import sys
import math
import json

pygame.init()

def read_model(path):
    with open(path, "r") as file:
        data = json.load(file)
    return data

class SoftBody:
    def __init__(self, bounce=0.9, gravity=0.2, friction=0.999):
        self.bounce = bounce
        self.gravity = gravity
        self.friction = friction
        self.points = []
        self.sticks = []
    
    def load_model(self, model, offset=(0, 0)):
        self.points.clear()
        for point in model["points"]:
            self.add_point(
                point["x"] * model["scale"] + offset[0],
                point["y"] * model["scale"] + offset[1],
                point["locked"])

        self.sticks.clear()
        for connection in model["connections"]:
            self.add_stick(
                self.points[connection[0]], 
                self.points[connection[1]])

    def add_point(self, x, y, locked=False):
        self.points.append({
            "x": x,
            "y": y,
            "lastx": x,
            "lasty": y,
            "locked": locked
        })

    def add_stick(self, p1, p2):
        self.sticks.append({
            "p1": p1,
            "p2": p2,
            "length": math.dist((p1["x"], p1["y"]), (p2["x"], p2["y"])) 
        })

    def update_points(self):
        for point in self.points:
            if point["locked"]:
                continue

            velx = (point["x"] - point["lastx"]) * self.friction
            vely = (point["y"] - point["lasty"]) * self.friction

            point["lastx"] = point["x"]
            point["lasty"] = point["y"]

            point["x"] += velx
            point["y"] += vely
            point["y"] += self.gravity

    def update_sticks(self):
        for stick in self.sticks:
            distx = stick["p1"]["x"] - stick["p2"]["x"]
            disty = stick["p1"]["y"] - stick["p2"]["y"]

            distance = math.sqrt(distx**2 + disty**2)
            difference = stick["length"] - distance

            try:
                percent = difference / distance / 2
            except ZeroDivisionError:
                percent = 0

            offsetx = distx * percent
            offsety = disty * percent

            if not stick["p1"]["locked"]:
                stick["p1"]["x"] += offsetx
                stick["p1"]["y"] += offsety
            if not stick["p2"]["locked"]:
                stick["p2"]["x"] -= offsetx
                stick["p2"]["y"] -= offsety

    def render_points(self, surface):
        for point in self.points:
            pygame.draw.circle(surface, (0, 0, 0), (point["x"], point["y"]), 2)

    def render_sticks(self, surface):
        for stick in self.sticks:
            pygame.draw.aaline(surface, (0, 0, 0), (stick["p1"]["x"], stick["p1"]["y"]), (stick["p2"]["x"], stick["p2"]["y"]))

class Chain(SoftBody):
    def __init__(self, points, bounce=0.9, gravity=0.2, friction=0.999):
        super().__init__(bounce=bounce, gravity=gravity, friction=friction)
        for point in points:
            self.add_point(point[0], point[1])
        for i in range(len(self.points)):
            if i > len(self.points) - 2:
                break
            self.add_stick(self.points[i], self.points[i + 1])

class Cloth(SoftBody):
    def __init__(self, x, y, width, height, length, bounce=0.9, gravity=0.2, friction=0.999):
        super().__init__(bounce=bounce, gravity=gravity, friction=friction)
        self.lengthx = int(width / length)
        self.lengthy = int(height / length)

        for _y in range(y, y + height, length):
            for _x in range(x, x + width, length):
                self.add_point(_x, _y)
        for i in range(0, self.lengthx * self.lengthy, self.lengthx):
            for x in range(i, i + self.lengthx - 1):
                self.add_stick(self.points[x], self.points[x + 1])
        for i in range(-self.lengthx, 0):
            for y in range(i, self.lengthx * self.lengthy - self.lengthx * 2, self.lengthx):
                self.add_stick(self.points[y + self.lengthx], self.points[y + self.lengthx * 2])
        for point in self.points[0:self.lengthx:5]:
            point["locked"] = True

SCREEN_WIDTH = 480
SCREEN_HEIGHT = 640
SCREEN = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
CLOCK = pygame.time.Clock()
FONT = pygame.font.SysFont("comicsans", 14)

pygame.display.set_caption("Verlet Intergration")

cloth = (Cloth(150, 100, 180, 200, 5))

paused = True
render_points = False
render_sticks = True
held_points = []

def update():
    cloth.update_points()
    for _ in range(3):
        cloth.update_sticks()

def render(points=False, sticks=True):
    if points: cloth.render_points(SCREEN)
    if sticks: cloth.render_sticks(SCREEN)

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.MOUSEBUTTONDOWN:
            for point in cloth.points:
                if math.dist((point["x"], point["y"]), event.pos) < 5:
                    held_points.append(point)
        elif event.type == pygame.MOUSEBUTTONUP:
            held_points.clear()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                paused = not paused
            elif event.key == pygame.K_n:
                render_points = not render_points
            elif event.key == pygame.K_m:
                render_sticks = not render_sticks
            elif event.key == pygame.K_p:
                render_polygon = not render_polygon

    SCREEN.fill((255, 255, 255))

    mx, my = pygame.mouse.get_rel()

    for point in held_points:
        point["x"] += mx
        point["y"] += my

    if not paused:
        update()
    render(render_points, render_sticks)

    fps_label = FONT.render("fps: " + str(round(CLOCK.get_fps(), 2)), True, (0, 0, 0))
    SCREEN.blit(fps_label, (10, 10))

    pygame.display.update()

    CLOCK.tick(60)
