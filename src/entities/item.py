from src.entities.entity import Entity
from src.core.constants import (
    BUTTON_COLOR, NEEDLE_COLOR, KEY_COLOR,
    SCORE_BUTTON, SCORE_NEEDLE, SCORE_KEY,
)


class Item(Entity):
    """Базовый предмет."""

    def __init__(self, tx, ty, color):
        super().__init__(tx, ty, color)

    def on_pickup(self, player):
        pass


class Button(Item):
    """Пуговица — лечит на 1 HP."""

    def __init__(self, tx, ty):
        super().__init__(tx, ty, BUTTON_COLOR)

    def on_pickup(self, player):
        player.heal(1)
        player.buttons += 1
        player.score += SCORE_BUTTON


class Needle(Item):
    """Иголка — +1 урона."""

    def __init__(self, tx, ty):
        super().__init__(tx, ty, NEEDLE_COLOR)

    def on_pickup(self, player):
        player.attack_damage += 1
        player.buttons += 1
        player.score += SCORE_NEEDLE


class Key(Item):
    """Ключ — открывает выход."""

    def __init__(self, tx, ty):
        super().__init__(tx, ty, KEY_COLOR)

    def on_pickup(self, player):
        player.has_key = True
        player.score += SCORE_KEY
