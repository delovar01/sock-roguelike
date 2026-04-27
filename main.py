import pygame

from src.core.constants import SCREEN_WIDTH, SCREEN_HEIGHT, FPS, WINDOW_TITLE, BG_COLOR, TILE_SIZE, PLAYER_SPEED


def main():
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption(WINDOW_TITLE)
    clock = pygame.time.Clock()

    x = 100
    y = 100
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        keys = pygame.key.get_pressed()
        if keys[pygame.K_w] or keys[pygame.K_UP]:
            y -= PLAYER_SPEED
        if keys[pygame.K_s] or keys[pygame.K_DOWN]:
            y += PLAYER_SPEED
        if keys[pygame.K_a] or keys[pygame.K_LEFT]:
            x -= PLAYER_SPEED
        if keys[pygame.K_d] or keys[pygame.K_RIGHT]:
            x += PLAYER_SPEED
        screen.fill(BG_COLOR)
        pygame.draw.rect(screen, (220, 220, 220), (x, y, TILE_SIZE, TILE_SIZE))
        pygame.display.flip()
        clock.tick(FPS)

    pygame.quit()


if __name__ == "__main__":
    main()
