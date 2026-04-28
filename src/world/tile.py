from src.core.constants import TILE_SIZE


def tile_to_world(tx, ty):
    """Координаты тайла -> координаты пикселей (левый верх клетки)."""
    return tx * TILE_SIZE, ty * TILE_SIZE


def world_to_tile(x, y):
    """Координаты пикселей -> координаты тайла."""
    return x // TILE_SIZE, y // TILE_SIZE
