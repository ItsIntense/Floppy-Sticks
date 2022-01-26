import pygame
import sys

pygame.init()

SCREEN = pygame.display.set_mode((920, 640))

state = "clickable"
image = pygame.Surface((60, 60))
image.set_colorkey((0, 0, 0))
match state:
    case "static":
        pygame.draw.circle(image, (40, 160, 200), (30, 30), 30)
        pygame.draw.circle(image, (255, 255, 255), (30, 30), 30, width=6)
    case "dynamic":
        pygame.draw.circle(image, (255, 255, 255), (30, 30), 30)
    case "clickable":
        pygame.draw.circle(image, (10, 20, 30), (30, 30), 30)
        pygame.draw.circle(image, (255, 255, 255), (30, 30), 30, width=6)
        pygame.draw.circle(image, (255, 255, 255), (30, 30), 14)
    case _:
        image.fill((255, 255, 255))
# image = pygame.transform.smoothscale(image.copy(), (20, 20))
# pygame.image.save(image,state + ".png")
# image = pygame.image.load(state + ".png")

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    SCREEN.fill((0, 255, 255))

    SCREEN.blit(image, (200, 200))

    pygame.display.update()
