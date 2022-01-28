import pygame

def generate(state):
    image = pygame.Surface((60, 60), flags=pygame.SRCALPHA)
    match state:
        case "static":
            pygame.draw.circle(image, (255, 0, 130), (30, 30), 30)
            pygame.draw.circle(image, (255, 255, 255), (30, 30), 30, width=6)
        case "dynamic":
            pygame.draw.circle(image, (255, 255, 255), (30, 30), 30)
        case "clickable":
            pygame.draw.circle(image, (10, 20, 30), (30, 30), 30)
            pygame.draw.circle(image, (255, 255, 255), (30, 30), 30, width=6)
            pygame.draw.circle(image, (255, 255, 255), (30, 30), 14)
        case _:
            image.fill((255, 255, 255))
    image = pygame.transform.smoothscale(image, (20, 20))
    pygame.image.save(image, "assets/images/" + state + ".png")

if __name__ == "__main__":
    generate("static")
    generate("dynamic")
    generate("clickable")
