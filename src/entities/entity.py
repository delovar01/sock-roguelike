import pygame

from src.core.constants import TILE_SIZE


class Entity:
    """Базовый класс для всего что есть в мире.

    Хранит позицию в тайлах, не в пикселях.
    """

    def __init__(self, tx, ty, color):
        self.tx = tx
        self.ty = ty
        self.color = color
        self.alive = True

    def set_position(self, tx, ty):
        self.tx = tx
        self.ty = ty

    @property
    def position(self):
        return (self.tx, self.ty)

    def get_rect(self):
        return pygame.Rect(self.tx * TILE_SIZE, self.ty * TILE_SIZE,
                           TILE_SIZE, TILE_SIZE)

    def update(self, dt, world):
        # переопределяется в наследниках
        pass

    def draw(self, surface, camera):
        x = self.tx * TILE_SIZE - camera.offset_x
        y = self.ty * TILE_SIZE - camera.offset_y
        pygame.draw.rect(surface, self.color, (x + 4, y + 4, TILE_SIZE - 8, TILE_SIZE - 8))
