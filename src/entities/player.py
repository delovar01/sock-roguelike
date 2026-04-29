from src.entities.entity import Entity
from src.core.constants import PLAYER_COLOR, PLAYER_MAX_HP


class Player(Entity):
    """Игрок-носок. HP инкапсулирован: снаружи только через property."""

    def __init__(self, tx, ty):
        super().__init__(tx, ty, PLAYER_COLOR)
        self._hp = PLAYER_MAX_HP
        self._buttons = 0
        self._invuln_timer = 0.0  # короткая неуязвимость после удара

    @property
    def hp(self):
        return self._hp

    @property
    def buttons(self):
        return self._buttons

    @property
    def is_invulnerable(self):
        return self._invuln_timer > 0

    def take_damage(self, amount=1):
        if self._invuln_timer > 0:
            return False
        self._hp = max(0, self._hp - amount)
        self._invuln_timer = 0.8
        return True

    def heal(self, amount=1):
        if self._hp >= PLAYER_MAX_HP:
            return False
        self._hp = min(PLAYER_MAX_HP, self._hp + amount)
        return True

    def add_button(self):
        self._buttons += 1

    def is_dead(self):
        return self._hp <= 0

    def update(self, dt, world):
        if self._invuln_timer > 0:
            self._invuln_timer -= dt

    def set_state(self, hp, buttons):
        # для загрузки сохранений
        self._hp = hp
        self._buttons = buttons
