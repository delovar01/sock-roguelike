import pygame

from src.scenes.base_scene import BaseScene
from src.core.constants import SCREEN_WIDTH, SCREEN_HEIGHT, HUD_COLOR, MENU


def _format_time(seconds):
    m = int(seconds) // 60
    s = int(seconds) % 60
    return f"{m:02d}:{s:02d}"


class WinScene(BaseScene):
    def __init__(self, game, stats=None):
        super().__init__(game)
        self.big = game.resources.get_font(48)
        self.med = game.resources.get_font(26)
        self.small = game.resources.get_font(22)
        self.stats = stats or {}

    def handle_event(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key in (pygame.K_RETURN, pygame.K_SPACE, pygame.K_ESCAPE):
                self.game.change_scene(MENU)

    def update(self, dt):
        pass

    def draw(self, surface):
        cx = SCREEN_WIDTH // 2
        cy = SCREEN_HEIGHT // 2
        title = self.big.render("Носок нашёл свою пару!", True, (200, 230, 130))
        surface.blit(title, title.get_rect(center=(cx, cy - 140)))

        score = self.stats.get("score", 0)
        kills = self.stats.get("kills", 0)
        buttons = self.stats.get("buttons", 0)
        tm = self.stats.get("time", 0.0)

        lines = [
            f"Итоговый счёт: {score}",
            "",
            f"Убито врагов: {kills}",
            f"Собрано предметов: {buttons}",
            f"Время прохождения: {_format_time(tm)}",
        ]
        for i, line in enumerate(lines):
            s = self.med.render(line, True, HUD_COLOR)
            surface.blit(s, s.get_rect(center=(cx, cy - 60 + i * 32)))

        hint = self.small.render("Enter — в меню", True, (180, 180, 180))
        surface.blit(hint, hint.get_rect(center=(cx, cy + 160)))
