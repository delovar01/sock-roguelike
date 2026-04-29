from abc import ABC, abstractmethod

import pygame

from src.core.constants import TILE_SIZE


class Entity(ABC):
    """Базовый абстрактный класс для всего что есть в мире.

    Хранит позицию в тайлах (tx, ty), не в пикселях.
    """

    def __init__(self, tx, ty, color):
        self._tx = tx
        self._ty = ty
        self._color = color
        self.alive = True

    @property
    def tx(self):
        return self._tx

    @property
    def ty(self):
        return self._ty

    @property
    def position(self):
        return (self._tx, self._ty)

    def set_position(self, tx, ty):
        self._tx = tx
        self._ty = ty

    def get_rect(self):
        return pygame.Rect(self._tx * TILE_SIZE, self._ty * TILE_SIZE,
                           TILE_SIZE, TILE_SIZE)

    @abstractmethod
    def update(self, dt, world):
        ...

    def draw(self, surface, camera):
        x = self._tx * TILE_SIZE - camera.offset_x
        y = self._ty * TILE_SIZE - camera.offset_y
        pygame.draw.rect(surface, self._color, (x + 4, y + 4, TILE_SIZE - 8, TILE_SIZE - 8))
