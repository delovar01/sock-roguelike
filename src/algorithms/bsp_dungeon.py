"""BSP генератор подземелья.

Разбиение работает. Теперь добавил комнаты в листьях.
Коридоров пока нет.
"""

import random

from src.core.constants import (
    BSP_MIN_LEAF_SIZE, BSP_MAX_DEPTH, ROOM_MIN_SIZE, ROOM_PADDING
)


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
