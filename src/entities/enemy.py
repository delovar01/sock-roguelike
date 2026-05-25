from src.entities.entity import Entity
from src.core.constants import (
    ENEMY_COLOR, SPIDER_COLOR,
    PATROL, CHASE, RETURN,
    DETECT_RADIUS, LOSE_RADIUS,
    SPIDER_DETECT_RADIUS, SPIDER_LOSE_RADIUS,
    MOTH_HP, SPIDER_HP,
)


class Enemy(Entity):
    """Враг. Поведение через автомат PATROL -> CHASE -> RETURN."""

    def __init__(self, tx, ty, waypoints, hp=MOTH_HP,
                 detect_radius=DETECT_RADIUS, lose_radius=LOSE_RADIUS,
                 move_period=0.35, color=ENEMY_COLOR):
        super().__init__(tx, ty, color)
        self.hp = hp
        self.detect_radius = detect_radius
        self.lose_radius = lose_radius
        self.waypoints = list(waypoints) if waypoints else [(tx, ty)]
        self.wp_index = 0
        self.state = PATROL
        self.path = []
        self.move_cooldown = 0.0
        self.move_period = move_period
        self.repath_cooldown = 0.0

    def set_path(self, path):
        self.path = list(path)

    def take_damage(self, dmg):
        self.hp -= dmg
        if self.hp <= 0:
            self.alive = False

    def should_repath(self, dt):
        self.repath_cooldown -= dt
        if self.repath_cooldown <= 0:
            self.repath_cooldown = 0.25
            return True
        return False

    def distance_to(self, tx, ty):
        return abs(self.tx - tx) + abs(self.ty - ty)

    def update_fsm(self, player_tx, player_ty):
        dist = self.distance_to(player_tx, player_ty)
        if self.state == PATROL:
            if dist <= self.detect_radius:
                self.state = CHASE
        elif self.state == CHASE:
            if dist > self.lose_radius:
                self.state = RETURN
        elif self.state == RETURN:
            wp = self.waypoints[self.wp_index]
            if self.tx == wp[0] and self.ty == wp[1]:
                self.state = PATROL

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


class Spider(Enemy):
    """Паук. Быстрее моли, видит ближе, HP меньше."""

    def __init__(self, tx, ty, waypoints):
        super().__init__(
            tx, ty, waypoints,
            hp=SPIDER_HP,
            detect_radius=SPIDER_DETECT_RADIUS,
            lose_radius=SPIDER_LOSE_RADIUS,
            move_period=0.22,
            color=SPIDER_COLOR,
        )
