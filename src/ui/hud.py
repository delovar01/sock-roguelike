import pygame

from src.core.constants import HUD_COLOR, PLAYER_MAX_HP


class Hud:
    """Полоска HP, счётчик пуговиц, номер уровня."""

    def __init__(self, resources):
        self.font = resources.get_font(22)

    def draw(self, surface, player, level_num):
        # HP — три квадратика сверху слева
        for i in range(PLAYER_MAX_HP):
            x = 12 + i * 28
            y = 12
            if i < player.hp:
                color = (220, 80, 80)
            else:
                color = (90, 90, 90)
            pygame.draw.rect(surface, color, (x, y, 24, 24))
            pygame.draw.rect(surface, HUD_COLOR, (x, y, 24, 24), 1)

        # пуговицы
        text = self.font.render(f"Пуговицы: {player.buttons}", True, HUD_COLOR)
        surface.blit(text, (12, 48))

        # уровень
        lvl_text = self.font.render(f"Уровень {level_num}", True, HUD_COLOR)
        surface.blit(lvl_text, (surface.get_width() - lvl_text.get_width() - 12, 12))
