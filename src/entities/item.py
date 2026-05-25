from src.entities.entity import Entity
from src.core.constants import ITEM_COLOR


class Item(Entity):
    """Пуговица. Подбирается, восстанавливает 1 HP."""

    def __init__(self, tx, ty):
        super().__init__(tx, ty, ITEM_COLOR)
