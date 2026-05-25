import pygame

from src.core.constants import (
    TILE_SIZE, PATROL, CHASE, RETURN,
    LIGHT_RADIUS, LIGHT_FADE, LIGHT_DARKNESS,
)


# цвета для отладки состояния врагов
STATE_COLORS = {
    PATROL: (80, 200, 80),
    CHASE: (240, 180, 40),
    RETURN: (80, 140, 240),
}


class RenderSystem:
    """Рисует мир и сущности."""

    def __init__(self):
        self.debug = False

    def toggle_debug(self):
        self.debug = not self.debug

    def draw(self, surface, level, entities, camera):
        level.draw(surface, camera)
        for e in entities:
            if e.alive:
                e.draw(surface, camera)

    def draw_lighting(self, surface, player, camera):
        """Тёмный слой с дыркой вокруг игрока — эффект факела."""
        dark = pygame.Surface(surface.get_size(), pygame.SRCALPHA)
        dark.fill((0, 0, 0, LIGHT_DARKNESS))
        px = player.tx * TILE_SIZE - camera.offset_x + TILE_SIZE // 2
        py = player.ty * TILE_SIZE - camera.offset_y + TILE_SIZE // 2
        pygame.draw.circle(dark, (0, 0, 0, 0), (px, py), LIGHT_RADIUS)
        pygame.draw.circle(
            dark, (0, 0, 0, LIGHT_DARKNESS // 2),
            (px, py), LIGHT_RADIUS + LIGHT_FADE, width=LIGHT_FADE,
        )
        surface.blit(dark, (0, 0))

    def draw_enemy_hp(self, surface, enemies, camera):
        """Полоска HP над раненым врагом."""
        for enemy in enemies:
            if not enemy.alive:
                continue
            max_hp = getattr(enemy, "_max_hp", None)
            if max_hp is None:
                max_hp = enemy.hp
                enemy._max_hp = max_hp
            if enemy.hp >= max_hp:
                continue
            ex = enemy.tx * TILE_SIZE - camera.offset_x
            ey = enemy.ty * TILE_SIZE - camera.offset_y
            pygame.draw.rect(surface, (60, 0, 0), (ex + 4, ey - 6, TILE_SIZE - 8, 4))
            w = int((TILE_SIZE - 8) * enemy.hp / max_hp)
            pygame.draw.rect(surface, (220, 60, 60), (ex + 4, ey - 6, w, 4))

    def draw_debug(self, surface, enemies, camera, fps):
        if not self.debug:
            return
        for enemy in enemies:
            if not enemy.alive:
                continue
            ex = enemy.tx * TILE_SIZE - camera.offset_x
            ey = enemy.ty * TILE_SIZE - camera.offset_y
            pygame.draw.rect(surface, (255, 255, 255), (ex, ey, TILE_SIZE, TILE_SIZE), 1)
            state_color = STATE_COLORS.get(enemy.state, (200, 200, 200))
            pygame.draw.circle(surface, state_color, (ex + 6, ey + 6), 5)
            for tx, ty in enemy.path:
                x = tx * TILE_SIZE - camera.offset_x + TILE_SIZE // 2
                y = ty * TILE_SIZE - camera.offset_y + TILE_SIZE // 2
                pygame.draw.circle(surface, (255, 80, 80), (x, y), 4)
        font = pygame.font.SysFont("Arial", 16)
        text = font.render("FPS: " + str(int(fps)), True, (255, 255, 255))
        surface.blit(text, (surface.get_width() - 80, surface.get_height() - 24))
