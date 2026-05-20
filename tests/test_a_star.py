from src.algorithms.a_star import find_path, manhattan
from src.core.constants import TileType
from src.world.level import Level


def _empty_level(w, h):
    grid = [[TileType.FLOOR for _ in range(w)] for _ in range(h)]
    return Level(grid, (0, 0), (w - 1, h - 1))


def test_finds_direct_path_in_empty_grid():
    level = _empty_level(5, 5)
    path = find_path(level, (0, 0), (4, 4))
    # манхэттенский путь длиной 8 (4 шага вправо + 4 шага вниз)
    assert len(path) == 8


def test_avoids_walls():
    grid = [[TileType.FLOOR for _ in range(5)] for _ in range(5)]
    # стена посередине
    for y in range(0, 4):
        grid[y][2] = TileType.WALL
    level = Level(grid, (0, 0), (4, 4))
    path = find_path(level, (0, 0), (4, 0))
    # путь существует, но обходит стену снизу
    assert len(path) > 0
    assert (2, 0) not in path  # не идём сквозь стену


def test_returns_empty_when_unreachable():
    grid = [[TileType.FLOOR for _ in range(5)] for _ in range(5)]
    for x in range(5):
        grid[2][x] = TileType.WALL  # горизонтальная стена пополам
    level = Level(grid, (0, 0), (4, 4))
    path = find_path(level, (0, 0), (0, 4))
    assert path == []


def test_manhattan():
    assert manhattan((0, 0), (3, 4)) == 7
    assert manhattan((5, 5), (5, 5)) == 0
