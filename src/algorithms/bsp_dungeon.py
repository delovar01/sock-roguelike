"""BSP-генератор подземелья.

Binary Space Partitioning. Рекурсивно делим пространство, в каждом
листе размещаем комнату, соединяем L-образными коридорами.

Сложность O(n) по числу клеток.
"""

import random

from src.core.constants import (
    TileType, BSP_MIN_LEAF_SIZE, BSP_MAX_DEPTH,
    ROOM_MIN_SIZE, ROOM_PADDING
)


# первая попытка была просто одной большой комнатой посреди карты
# def naive_room(w, h):
#     g = [[TileType.WALL for _ in range(w)] for _ in range(h)]
#     for y in range(2, h-2):
#         for x in range(2, w-2):
#             g[y][x] = TileType.FLOOR
#     return g


class BSPNode:
    def __init__(self, x, y, w, h):
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.left = None
        self.right = None
        self.room = None

    def is_leaf(self):
        return self.left is None and self.right is None

    def center(self):
        if self.room is None:
            return (self.x + self.w // 2, self.y + self.h // 2)
        rx, ry, rw, rh = self.room
        return (rx + rw // 2, ry + rh // 2)


def split_node(node, rng, depth):
    if depth >= BSP_MAX_DEPTH:
        return False
    if node.w > node.h:
        split_vertical = True
    elif node.h > node.w:
        split_vertical = False
    else:
        split_vertical = rng.random() < 0.5
    min_size = BSP_MIN_LEAF_SIZE
    if split_vertical:
        if node.w < min_size * 2:
            return False
        split_at = rng.randint(min_size, node.w - min_size)
        node.left = BSPNode(node.x, node.y, split_at, node.h)
        node.right = BSPNode(node.x + split_at, node.y, node.w - split_at, node.h)
    else:
        if node.h < min_size * 2:
            return False
        split_at = rng.randint(min_size, node.h - min_size)
        node.left = BSPNode(node.x, node.y, node.w, split_at)
        node.right = BSPNode(node.x, node.y + split_at, node.w, node.h - split_at)
    split_node(node.left, rng, depth + 1)
    split_node(node.right, rng, depth + 1)
    return True


def create_room_in_leaf(leaf, rng):
    max_w = leaf.w - ROOM_PADDING * 2
    max_h = leaf.h - ROOM_PADDING * 2
    if max_w < ROOM_MIN_SIZE or max_h < ROOM_MIN_SIZE:
        return
    rw = rng.randint(ROOM_MIN_SIZE, max_w)
    rh = rng.randint(ROOM_MIN_SIZE, max_h)
    rx = leaf.x + rng.randint(ROOM_PADDING, leaf.w - rw - ROOM_PADDING)
    ry = leaf.y + rng.randint(ROOM_PADDING, leaf.h - rh - ROOM_PADDING)
    leaf.room = (rx, ry, rw, rh)


def fill_rooms(node, rng):
    if node.is_leaf():
        create_room_in_leaf(node, rng)
        return
    fill_rooms(node.left, rng)
    fill_rooms(node.right, rng)


def _safe_carve(grid, x, y):
    if 0 <= y < len(grid) and 0 <= x < len(grid[0]):
        grid[y][x] = TileType.FLOOR


def carve_rooms_to_grid(node, grid):
    if node.is_leaf():
        if node.room is None:
            return
        rx, ry, rw, rh = node.room
        for y in range(ry, ry + rh):
            for x in range(rx, rx + rw):
                _safe_carve(grid, x, y)
        return
    carve_rooms_to_grid(node.left, grid)
    carve_rooms_to_grid(node.right, grid)


def carve_l_corridor(grid, a, b, rng):
    ax, ay = a
    bx, by = b
    if rng.random() < 0.5:
        for x in range(min(ax, bx), max(ax, bx) + 1):
            _safe_carve(grid, x, ay)
        for y in range(min(ay, by), max(ay, by) + 1):
            _safe_carve(grid, bx, y)
    else:
        for y in range(min(ay, by), max(ay, by) + 1):
            _safe_carve(grid, ax, y)
        for x in range(min(ax, bx), max(ax, bx) + 1):
            _safe_carve(grid, x, by)


def get_any_room_center(node):
    if node.is_leaf():
        if node.room is None:
            return None
        return node.center()
    c = get_any_room_center(node.left)
    if c is not None:
        return c
    return get_any_room_center(node.right)


def connect_rooms(node, grid, rng):
    if node.is_leaf():
        return
    connect_rooms(node.left, grid, rng)
    connect_rooms(node.right, grid, rng)
    c1 = get_any_room_center(node.left)
    c2 = get_any_room_center(node.right)
    if c1 is None or c2 is None:
        return
    carve_l_corridor(grid, c1, c2, rng)


def collect_room_centers(node, out):
    if node.is_leaf():
        if node.room is not None:
            out.append(node.center())
        return
    collect_room_centers(node.left, out)
    collect_room_centers(node.right, out)


def generate(width, height, seed):
    rng = random.Random(seed)
    grid = [[TileType.WALL for _ in range(width)] for _ in range(height)]
    root = BSPNode(0, 0, width, height)
    split_node(root, rng, 0)
    fill_rooms(root, rng)
    carve_rooms_to_grid(root, grid)
    connect_rooms(root, grid, rng)

    centers = []
    collect_room_centers(root, centers)
    if not centers:
        spawn = (width // 2, height // 2)
        exit_pos = (width // 2 + 1, height // 2)
        _safe_carve(grid, *spawn)
        _safe_carve(grid, *exit_pos)
        grid[exit_pos[1]][exit_pos[0]] = TileType.EXIT
        return grid, spawn, exit_pos

    spawn = centers[0]
    exit_pos = max(centers[1:], default=centers[0],
                   key=lambda c: abs(c[0] - spawn[0]) + abs(c[1] - spawn[1]))
    grid[exit_pos[1]][exit_pos[0]] = TileType.EXIT
    return grid, spawn, exit_pos
