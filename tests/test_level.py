from src.world.level import Level
from src.core.constants import TileType


def test_is_walkable_returns_false_for_wall():
    grid = [[TileType.WALL, TileType.FLOOR],
            [TileType.FLOOR, TileType.WALL]]
    level = Level(grid, (1, 0), (0, 1))
    assert level.is_walkable(0, 0) is False
    assert level.is_walkable(1, 0) is True


def test_get_tile_out_of_bounds_returns_wall():
    grid = [[TileType.FLOOR]]
    level = Level(grid, (0, 0), (0, 0))
    assert level.get_tile(-1, 0) == TileType.WALL
    assert level.get_tile(0, 5) == TileType.WALL
