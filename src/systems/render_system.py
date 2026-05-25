import pygame

from src.core.constants import TILE_SIZE, EnemyState


# цвета для отладки врагов по их состоянию
# (методичка про debug так и советует)
STATE_COLORS = {
    EnemyState.PATROL: (80, 200, 80),
    EnemyState.CHASE: (240, 180, 40),
    EnemyState.RETURN: (80, 140, 240),
}


class RenderSystem:
    """Рисует мир и сущности. Логики нет, только отрисовка."""

    def __init__(self):
        self.debug = False

    def toggle_debug(self):
        self.debug = not self.debug

    def draw(self, surface, level, entities, camera):
        level.draw(surface, camera)
        for e in entities:
            if e.alive:
                e.draw(surface, camera)

    def draw_enemy_hp(self, surface, enemies, camera):
        """Полоска HP над каждым раненым врагом."""
        for enemy in enemies:
            if not enemy.alive:
                continue
            # не показываем у полностью здоровых — чтобы не засорять экран
            max_hp = getattr(enemy, "_max_hp", None)
            if max_hp is None:
                max_hp = enemy.hp  # запомнить как видели первый раз
                enemy._max_hp = max_hp
            if enemy.hp >= max_hp:
                continue
            ex = enemy.tx * TILE_SIZE - camera.offset_x
            ey = enemy.ty * TILE_SIZE - camera.offset_y
            # фон полоски
            pygame.draw.rect(surface, (60, 0, 0), (ex + 4, ey - 6, TILE_SIZE - 8, 4))
            # заполнение по HP
            w = int((TILE_SIZE - 8) * enemy.hp / max_hp)
            pygame.draw.rect(surface, (220, 60, 60), (ex + 4, ey - 6, w, 4))

    def draw_debug(self, surface, enemies, camera, fps):
        # вся отладка только если включена клавишей F3
        if not self.debug:
            return

        for enemy in enemies:
            if not enemy.alive:
                continue

            # хитбокс врага — рамка по тайлу
            ex = enemy.tx * TILE_SIZE - camera.offset_x
            ey = enemy.ty * TILE_SIZE - camera.offset_y
            pygame.draw.rect(surface, (255, 255, 255), (ex, ey, TILE_SIZE, TILE_SIZE), 1)

            # цветовое кодирование состояния
            state_color = STATE_COLORS.get(enemy.state, (200, 200, 200))
            pygame.draw.circle(surface, state_color, (ex + 6, ey + 6), 5)

            # путь A* красными точками
            for tx, ty in enemy.path:
                x = tx * TILE_SIZE - camera.offset_x + TILE_SIZE // 2
                y = ty * TILE_SIZE - camera.offset_y + TILE_SIZE // 2
                pygame.draw.circle(surface, (255, 80, 80), (x, y), 4)

        # FPS в правом нижнем углу
        font = pygame.font.SysFont("Arial", 16)
        text = font.render(f"FPS: {int(fps)}", True, (255, 255, 255))
        surface.blit(text, (surface.get_width() - 80, surface.get_height() - 24))
