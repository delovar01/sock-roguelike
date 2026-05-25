from src.entities.entity import Entity
from src.core.constants import PLAYER_COLOR, PLAYER_MAX_HP, PLAYER_BASE_DAMAGE


class Player(Entity):
    """Игрок-носок."""

    def __init__(self, tx, ty):
        super().__init__(tx, ty, PLAYER_COLOR)
        self.hp = PLAYER_MAX_HP
        self.buttons = 0
        self.invuln_timer = 0.0
        self.attack_damage = PLAYER_BASE_DAMAGE
        self.score = 0
        self.kills = 0
        self.has_key = False

    def take_damage(self, amount=1):
        if self.invuln_timer > 0:
            return False
        self.hp -= amount
        if self.hp < 0:
            self.hp = 0
        self.invuln_timer = 0.8
        return True

    def heal(self, amount=1):
        if self.hp >= PLAYER_MAX_HP:
            return False
        self.hp += amount
        if self.hp > PLAYER_MAX_HP:
            self.hp = PLAYER_MAX_HP
        return True

    def is_dead(self):
        return self.hp <= 0

    def update(self, dt, world):
        if self.invuln_timer > 0:
            self.invuln_timer -= dt
