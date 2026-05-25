from src.algorithms.bsp_dungeon import generate
from src.core.constants import TileType


def _flood_fill_count(grid, start):
    h = len(grid)
    w = len(grid[0])
    seen = set()
    stack = [start]
    while stack:
        x, y = stack.pop()
        if (x, y) in seen:
            continue
        if x < 0 or y < 0 or x >= w or y >= h:
            continue
        if grid[y][x] == TileType.WALL:
            continue
        seen.add((x, y))
        stack.extend([(x + 1, y), (x - 1, y), (x, y + 1), (x, y - 1)])
    return seen


def test_generator_returns_grid_of_correct_size():
    grid, spawn, exit_pos, rooms, centers = generate(40, 30, seed=1)
    assert len(grid) == 30
    assert all(len(row) == 40 for row in grid)


def test_same_seed_produces_same_dungeon():
    g1, _, _, _, _ = generate(40, 30, seed=42)
    g2, _, _, _, _ = generate(40, 30, seed=42)
    assert g1 == g2


def test_all_floors_are_connected():
    grid, spawn, exit_pos, _, _ = generate(40, 30, seed=7)
    floors = sum(1 for row in grid for t in row if t != TileType.WALL)
    seen = _flood_fill_count(grid, spawn)
    assert len(seen) == floors


def test_rooms_have_minimum_size():
    _, _, _, rooms, _ = generate(40, 30, seed=3)
    assert all(r[2] >= 4 and r[3] >= 4 for r in rooms)
