from src.entities.entity import Entity
from src.core.constants import ITEM_COLOR


class Item(Entity):
    """Подбираемый предмет — пуговица. Восстанавливает 1 HP."""

    def __init__(self, tx, ty):
        super().__init__(tx, ty, ITEM_COLOR)

    def update(self, dt, world):
        # предметы статичны
        pass
