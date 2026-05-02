import pygame

from src.core.constants import HUD_COLOR


class MenuButton:
    """Простая прямоугольная кнопка с подсветкой выделенной."""

    def __init__(self, text, action):
        self.text = text
        self.action = action


def draw_buttons(surface, font, buttons, selected_index, center_x, start_y, gap=50):
    for i, btn in enumerate(buttons):
        color = (255, 220, 120) if i == selected_index else HUD_COLOR
        text = font.render(btn.text, True, color)
        rect = text.get_rect(center=(center_x, start_y + i * gap))
        surface.blit(text, rect)


def draw_title(surface, font, text, center_x, y):
    surf = font.render(text, True, HUD_COLOR)
    rect = surf.get_rect(center=(center_x, y))
    surface.blit(surf, rect)
