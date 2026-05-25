from src.algorithms.a_star import find_path, manhattan
from src.core.constants import FLOOR, WALL
from src.world.level import Level


def empty_level(w, h):
    grid = [[FLOOR for _ in range(w)] for _ in range(h)]
    return Level(grid, (0, 0), (w - 1, h - 1))


def test_simple_path():
    level = empty_level(5, 5)
    path = find_path(level, (0, 0), (4, 4))
    assert len(path) == 8


def test_no_path_when_blocked():
    grid = [[FLOOR for _ in range(5)] for _ in range(5)]
    for x in range(5):
        grid[2][x] = WALL
    level = Level(grid, (0, 0), (4, 4))
    path = find_path(level, (0, 0), (0, 4))
    assert path == []


def test_manhattan():
    assert manhattan((0, 0), (3, 4)) == 7
