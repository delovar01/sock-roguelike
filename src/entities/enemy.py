import math

from src.entities.entity import Entity
from src.core.constants import ENEMY_COLOR


class Enemy(Entity):
    """Враг-моль. Патрулирует между двумя точками."""

    def __init__(self, tx, ty, waypoints=None):
        super().__init__(tx, ty, ENEMY_COLOR)
        self._waypoints = list(waypoints) if waypoints else [(tx, ty)]
        self._wp_index = 0
        self._move_cooldown = 0.0
        self._move_period = 0.35

    def current_waypoint(self):
        return self._waypoints[self._wp_index]

    def advance_waypoint(self):
        self._wp_index = (self._wp_index + 1) % len(self._waypoints)

    def can_step(self, dt):
        self._move_cooldown -= dt
        if self._move_cooldown <= 0:
            self._move_cooldown = self._move_period
            return True
        return False

    def update(self, dt, world):
        pass
