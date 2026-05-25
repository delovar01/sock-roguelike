"""Генератор подземелья через BSP (Binary Space Partitioning).

Идея: рекурсивно делим прямоугольник пополам, в каждом листе дерева
размещаем комнату, потом соединяем комнаты L-образными коридорами.
"""

import random

from src.core.constants import (
    WALL, FLOOR, EXIT,
    BSP_MIN_LEAF_SIZE, BSP_MAX_DEPTH,
    ROOM_MIN_SIZE, ROOM_PADDING,
)


# раньше пробовал просто одну большую комнату посреди карты, но это не
# подземелье а зал. оставил, чтобы не забыть как было плохо
# def naive_room(w, h):
#     g = [[WALL for _ in range(w)] for _ in range(h)]
#     for y in range(2, h-2):
#         for x in range(2, w-2):
#             g[y][x] = FLOOR
#     return g


class BSPNode:
    """Узел дерева. Лист если нет потомков."""

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

    def room_center(self):
        if self.room is None:
            return None
        rx, ry, rw, rh = self.room
        return (rx + rw // 2, ry + rh // 2)


def split_node(node, rng, depth):
    if depth >= BSP_MAX_DEPTH:
        return
    if node.w > node.h:
        split_vertical = True
    elif node.h > node.w:
        split_vertical = False
    else:
        split_vertical = rng.random() < 0.5

    min_size = BSP_MIN_LEAF_SIZE
    if split_vertical:
        if node.w < min_size * 2:
            return
        cut = rng.randint(min_size, node.w - min_size)
        node.left = BSPNode(node.x, node.y, cut, node.h)
        node.right = BSPNode(node.x + cut, node.y, node.w - cut, node.h)
    else:
        if node.h < min_size * 2:
            return
        cut = rng.randint(min_size, node.h - min_size)
        node.left = BSPNode(node.x, node.y, node.w, cut)
        node.right = BSPNode(node.x, node.y + cut, node.w, node.h - cut)

    split_node(node.left, rng, depth + 1)
    split_node(node.right, rng, depth + 1)


def make_rooms(node, rng):
    if node.is_leaf():
        # TODO: для уровней 2-3 можно делать комнаты побольше
        max_w = node.w - ROOM_PADDING * 2
        max_h = node.h - ROOM_PADDING * 2
        if max_w < ROOM_MIN_SIZE or max_h < ROOM_MIN_SIZE:
            return
        rw = rng.randint(ROOM_MIN_SIZE, max_w)
        rh = rng.randint(ROOM_MIN_SIZE, max_h)
        rx = node.x + rng.randint(ROOM_PADDING, node.w - rw - ROOM_PADDING)
        ry = node.y + rng.randint(ROOM_PADDING, node.h - rh - ROOM_PADDING)
        node.room = (rx, ry, rw, rh)
        return
    make_rooms(node.left, rng)
    make_rooms(node.right, rng)


def carve_rooms(node, grid):
    if node.is_leaf():
        if node.room is None:
            return
        rx, ry, rw, rh = node.room
        for y in range(ry, ry + rh):
            for x in range(rx, rx + rw):
                grid[y][x] = FLOOR
        return
    carve_rooms(node.left, grid)
    carve_rooms(node.right, grid)


def find_any_center(node):
    if node.is_leaf():
        return node.room_center()
    c = find_any_center(node.left)
    if c is not None:
        return c
    return find_any_center(node.right)


def carve_corridor(grid, a, b, rng):
    ax, ay = a
    bx, by = b
    if rng.random() < 0.5:
        for x in range(min(ax, bx), max(ax, bx) + 1):
            grid[ay][x] = FLOOR
        for y in range(min(ay, by), max(ay, by) + 1):
            grid[y][bx] = FLOOR
    else:
        for y in range(min(ay, by), max(ay, by) + 1):
            grid[y][ax] = FLOOR
        for x in range(min(ax, bx), max(ax, bx) + 1):
            grid[by][x] = FLOOR


def connect_tree(node, grid, rng):
    if node.is_leaf():
        return
    connect_tree(node.left, grid, rng)
    connect_tree(node.right, grid, rng)
    c1 = find_any_center(node.left)
    c2 = find_any_center(node.right)
    if c1 is not None and c2 is not None:
        carve_corridor(grid, c1, c2, rng)


def collect_rooms(node, out):
    if node.is_leaf():
        if node.room is not None:
            out.append(node.room)
        return
    collect_rooms(node.left, out)
    collect_rooms(node.right, out)


def generate(width, height, seed):
    rng = random.Random(seed)
    grid = [[WALL for _ in range(width)] for _ in range(height)]

    root = BSPNode(0, 0, width, height)
    split_node(root, rng, 0)
    make_rooms(root, rng)
    carve_rooms(root, grid)
    connect_tree(root, grid, rng)

    rooms = []
    collect_rooms(root, rooms)
    centers = [(r[0] + r[2] // 2, r[1] + r[3] // 2) for r in rooms]

    if not centers:
        spawn = (width // 2, height // 2)
        exit_pos = (width // 2 + 1, height // 2)
        grid[spawn[1]][spawn[0]] = FLOOR
        grid[exit_pos[1]][exit_pos[0]] = EXIT
        return grid, spawn, exit_pos, rooms, centers

    spawn = centers[0]
    exit_pos = spawn
    best = -1
    for c in centers[1:]:
        d = abs(c[0] - spawn[0]) + abs(c[1] - spawn[1])
        if d > best:
            best = d
            exit_pos = c
    grid[exit_pos[1]][exit_pos[0]] = EXIT
    return grid, spawn, exit_pos, rooms, centers
