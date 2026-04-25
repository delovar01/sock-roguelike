import pygame

pygame.init()
screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption("Носок-одиночка")
clock = pygame.time.Clock()

x = 100
y = 100

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    screen.fill((30, 30, 40))
    pygame.draw.rect(screen, (220, 80, 80), (x, y, 32, 32))
    pygame.display.flip()
    clock.tick(60)

pygame.quit()
