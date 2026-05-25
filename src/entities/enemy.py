import math  # вроде не использую, оставил пока

from src.entities.entity import Entity
from src.core.constants import (
    ENEMY_COLOR, EnemyState, DETECT_RADIUS, LOSE_RADIUS
)


class Enemy(Entity):
    """Враг-моль. Поведение через автомат Patrol -> Chase -> Return."""

    def __init__(self, tx, ty, waypoints):
        super().__init__(tx, ty, ENEMY_COLOR)
        self.waypoints = list(waypoints) if waypoints else [(tx, ty)]
        self.wp_index = 0
        self.state = EnemyState.PATROL
        self.path = []
        self.move_cooldown = 0.0
        self.move_period = 0.35
        self.repath_cooldown = 0.0

    def set_path(self, path):
        self.path = list(path)

    def should_repath(self, dt):
        self.repath_cooldown -= dt
        if self.repath_cooldown <= 0:
            self.repath_cooldown = 0.25
            return True
        return False

    def distance_to(self, tx, ty):
        # манхэттенское расстояние
        return abs(self.tx - tx) + abs(self.ty - ty)

    def update_fsm(self, player_tx, player_ty):
        dist = self.distance_to(player_tx, player_ty)
        if self.state == EnemyState.PATROL:
            if dist <= DETECT_RADIUS:
                self.state = EnemyState.CHASE
        elif self.state == EnemyState.CHASE:
            if dist > LOSE_RADIUS:
                self.state = EnemyState.RETURN
        elif self.state == EnemyState.RETURN:
            wp = self.waypoints[self.wp_index]
            if self.tx == wp[0] and self.ty == wp[1]:
                self.state = EnemyState.PATROL

    def current_waypoint(self):
        return self.waypoints[self.wp_index]

    def advance_waypoint(self):
        self.wp_index = (self.wp_index + 1) % len(self.waypoints)

    def can_step(self, dt):
        self.move_cooldown -= dt
        if self.move_cooldown <= 0:
            self.move_cooldown = self.move_period
            return True
        return False
