"""BSP генератор подземелья — попытка номер 1.

Пока работает только разбиение пространства, комнат нет.
"""

import random

from src.core.constants import BSP_MIN_LEAF_SIZE, BSP_MAX_DEPTH


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
    # TODO: понять почему дерево иногда пустое
    if depth >= BSP_MAX_DEPTH:
        return False
    if node.w > node.h:
        split_vertical = True
    else:
        split_vertical = False
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
