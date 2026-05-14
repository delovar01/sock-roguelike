import pygame

from src.core.constants import TILE_SIZE


class RenderSystem:
    """Рисует мир и сущности. Никакой логики, только отрисовка."""

    def __init__(self):
        self.debug = False

    def toggle_debug(self):
        self.debug = not self.debug

    def draw(self, surface, level, entities, camera):
        level.draw(surface, camera)
        for e in entities:
            if e.alive:
                e.draw(surface, camera)

    def draw_debug(self, surface, enemies, camera):
        if not self.debug:
            return
        for enemy in enemies:
            if not enemy.alive:
                continue
            # отрисовать путь A* как кружки
            for tx, ty in enemy.path:
                x = tx * TILE_SIZE - camera.offset_x + TILE_SIZE // 2
                y = ty * TILE_SIZE - camera.offset_y + TILE_SIZE // 2
                pygame.draw.circle(surface, (255, 80, 80), (x, y), 4)
