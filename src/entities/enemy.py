from src.entities.entity import Entity
from src.core.constants import ENEMY_COLOR


class Enemy(Entity):
    """Враг-моль. Пока только стоит на месте."""

    def __init__(self, tx, ty):
        super().__init__(tx, ty, ENEMY_COLOR)

    def update(self, dt, world):
        pass
