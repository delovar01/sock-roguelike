import pygame

pygame.init()
screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption("Носок-одиночка")
clock = pygame.time.Clock()

x = 100
y = 100
speed = 4

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    keys = pygame.key.get_pressed()
    if keys[pygame.K_w] or keys[pygame.K_UP]:
        y -= speed
    if keys[pygame.K_s] or keys[pygame.K_DOWN]:
        y += speed
    if keys[pygame.K_a] or keys[pygame.K_LEFT]:
        x -= speed
    if keys[pygame.K_d] or keys[pygame.K_RIGHT]:
        x += speed
    screen.fill((30, 30, 40))
    pygame.draw.rect(screen, (220, 220, 220), (x, y, 32, 32))
    pygame.display.flip()
    clock.tick(60)

pygame.quit()
