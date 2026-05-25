from src.entities.entity import Entity
from src.core.constants import PLAYER_COLOR, PLAYER_MAX_HP, PLAYER_BASE_DAMAGE


class Player(Entity):
    """Игрок-носок. HP инкапсулирован через _hp + property hp."""

    def __init__(self, tx, ty):
        super().__init__(tx, ty, PLAYER_COLOR)
        self._hp = PLAYER_MAX_HP
        self._buttons = 0
        self.invuln_timer = 0.0
        # урон растёт от подобранных иголок
        self.attack_damage = PLAYER_BASE_DAMAGE
        # очки и убийства — копятся за всю игру
        self.score = 0
        self.kills = 0
        # ключ для выхода — сбрасывается на каждом уровне
        self.has_key = False

    @property
    def hp(self):
        return self._hp

    @property
    def buttons(self):
        return self._buttons

    def take_damage(self, amount=1):
        if self.invuln_timer > 0:
            return False
        self._hp -= amount
        if self._hp < 0:
            self._hp = 0
        self.invuln_timer = 0.8
        return True

    def heal(self, amount=1):
        if self._hp >= PLAYER_MAX_HP:
            return False
        self._hp += amount
        if self._hp > PLAYER_MAX_HP:
            self._hp = PLAYER_MAX_HP
        return True

    def add_button(self):
        self._buttons += 1

    def add_attack(self, amount=1):
        self.attack_damage += amount

    def add_score(self, amount):
        self.score += amount

    def add_kill(self):
        self.kills += 1

    def is_dead(self):
        return self._hp <= 0

    def update(self, dt, world):
        if self.invuln_timer > 0:
            self.invuln_timer -= dt

    def set_state(self, hp, buttons, attack=None, score=0, kills=0):
        # используется при загрузке сохранения
        self._hp = hp
        self._buttons = buttons
        if attack is not None:
            self.attack_damage = attack
        self.score = score
        self.kills = kills
