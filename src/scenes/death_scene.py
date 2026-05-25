import pygame

from src.scenes.base_scene import BaseScene
from src.core.constants import SCREEN_WIDTH, SCREEN_HEIGHT, HUD_COLOR, MENU


class DeathScene(BaseScene):
    def __init__(self, game):
        super().__init__(game)
        self.big = game.resources.get_font(64)
        self.small = game.resources.get_font(22)

    def handle_event(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key in (pygame.K_RETURN, pygame.K_SPACE, pygame.K_ESCAPE):
                self.game.change_scene(MENU)

    def update(self, dt):
        pass

    def draw(self, surface):
        cx = SCREEN_WIDTH // 2
        cy = SCREEN_HEIGHT // 2
        title = self.big.render("Носок сожрала моль", True, (220, 100, 100))
        surface.blit(title, title.get_rect(center=(cx, cy - 40)))
        hint = self.small.render("Enter — в меню", True, HUD_COLOR)
        surface.blit(hint, hint.get_rect(center=(cx, cy + 40)))
