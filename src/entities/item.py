from src.entities.entity import Entity
from src.core.constants import BUTTON_COLOR, NEEDLE_COLOR, KEY_COLOR


class Item(Entity):
    """Базовый предмет. on_pickup переопределяется у потомков."""

    def __init__(self, tx, ty, color):
        super().__init__(tx, ty, color)

    def on_pickup(self, player):
        # каждый предмет по-своему действует на игрока
        pass


class Button(Item):
    """Пуговица — лечит на 1 HP."""

    def __init__(self, tx, ty):
        super().__init__(tx, ty, BUTTON_COLOR)

    def on_pickup(self, player):
        player.heal(1)
        player.add_button()
        player.add_score(10)


class Needle(Item):
    """Иголка — увеличивает урон игрока на 1 (навсегда)."""

    def __init__(self, tx, ty):
        super().__init__(tx, ty, NEEDLE_COLOR)

    def on_pickup(self, player):
        player.add_attack(1)
        player.add_button()  # тоже считается за подобранный предмет
        player.add_score(30)


class Key(Item):
    """Ключ. Без него выход закрыт."""

    def __init__(self, tx, ty):
        super().__init__(tx, ty, KEY_COLOR)

    def on_pickup(self, player):
        player.has_key = True
        player.add_score(20)
