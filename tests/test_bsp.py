from src.algorithms.bsp_dungeon import generate


def test_grid_size():
    grid, spawn, exit_pos, rooms, centers = generate(40, 30, seed=1)
    assert len(grid) == 30
    assert len(grid[0]) == 40


def test_same_seed_same_dungeon():
    g1, _, _, _, _ = generate(40, 30, seed=42)
    g2, _, _, _, _ = generate(40, 30, seed=42)
    assert g1 == g2


def test_rooms_not_too_small():
    _, _, _, rooms, _ = generate(40, 30, seed=3)
    for r in rooms:
        assert r[2] >= 4
        assert r[3] >= 4
