import pygame

from src.core.constants import HUD_COLOR, PLAYER_MAX_HP


def _format_time(seconds):
    m = int(seconds) // 60
    s = int(seconds) % 60
    return f"{m:02d}:{s:02d}"


class Hud:
    """Полоска HP, счётчик пуговиц, урон, очки, время, уровень, сообщения."""

    def __init__(self, resources):
        self.font = resources.get_font(22)
        self.msg_font = resources.get_font(28)

    def draw(self, surface, player, level_num,
             elapsed_time=0.0, message="", message_timer=0.0):
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

        # пуговицы, урон
        text = self.font.render(f"Пуговицы: {player.buttons}", True, HUD_COLOR)
        surface.blit(text, (12, 48))
        dmg = self.font.render(f"Урон: {player.attack_damage}", True, HUD_COLOR)
        surface.blit(dmg, (12, 74))

        # ключ
        if player.has_key:
            k = self.font.render("Ключ: есть", True, (230, 200, 80))
        else:
            k = self.font.render("Ключ: нет", True, (180, 180, 180))
        surface.blit(k, (12, 100))

        # уровень + очки + время справа сверху
        right = surface.get_width() - 12
        lvl = self.font.render(f"Уровень {level_num}", True, HUD_COLOR)
        surface.blit(lvl, (right - lvl.get_width(), 12))

        score = self.font.render(f"Очки: {player.score}", True, HUD_COLOR)
        surface.blit(score, (right - score.get_width(), 38))

        tm = self.font.render(f"Время: {_format_time(elapsed_time)}", True, HUD_COLOR)
        surface.blit(tm, (right - tm.get_width(), 64))

        # временное сообщение по центру внизу
        if message and message_timer > 0:
            m = self.msg_font.render(message, True, (255, 220, 100))
            bg = m.get_rect(center=(surface.get_width() // 2,
                                    surface.get_height() - 60))
            pad = bg.inflate(20, 12)
            pygame.draw.rect(surface, (40, 40, 50), pad)
            pygame.draw.rect(surface, (220, 200, 100), pad, 1)
            surface.blit(m, bg)
