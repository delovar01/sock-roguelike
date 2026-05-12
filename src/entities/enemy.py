import math

from src.entities.entity import Entity
from src.core.constants import (
    ENEMY_COLOR, EnemyState, DETECT_RADIUS, LOSE_RADIUS
)


class Enemy(Entity):
    """Враг-моль. Поведение через FSM Patrol -> Chase -> Return."""

    def __init__(self, tx, ty, waypoints):
        super().__init__(tx, ty, ENEMY_COLOR)
        # waypoints — список точек для патруля
        self._waypoints = list(waypoints) if waypoints else [(tx, ty)]
        self._wp_index = 0
        self._state = EnemyState.PATROL
        self._path = []           # путь от A*, тайл-координаты
        self._move_cooldown = 0.0
        self._move_period = 0.35  # период шага в секундах
        self._repath_cooldown = 0.0

    @property
    def state(self):
        return self._state

    @property
    def path(self):
        return self._path

    def set_path(self, path):
        self._path = list(path)

    def should_repath(self, dt):
        self._repath_cooldown -= dt
        if self._repath_cooldown <= 0:
            self._repath_cooldown = 0.25
            return True
        return False

    def distance_to(self, tx, ty):
        # манхэттенское расстояние в тайлах
        return abs(self._tx - tx) + abs(self._ty - ty)

    def update_fsm(self, player_tx, player_ty):
        dist = self.distance_to(player_tx, player_ty)
        if self._state == EnemyState.PATROL:
            if dist <= DETECT_RADIUS:
                self._state = EnemyState.CHASE
        elif self._state == EnemyState.CHASE:
            if dist > LOSE_RADIUS:
                self._state = EnemyState.RETURN
        elif self._state == EnemyState.RETURN:
            wp = self._waypoints[self._wp_index]
            if self._tx == wp[0] and self._ty == wp[1]:
                self._state = EnemyState.PATROL

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
        # реальная логика — в ai_system, тут только таймеры
        pass
