import pygame

from src.entities.player import Player
from src.entities.item import Item
from src.entities.enemy import Enemy
from src.systems.movement_system import MovementSystem
from src.systems.collision_system import CollisionSystem
from src.core.event_bus import EventBus
from src.core.constants import TileType
from src.world.level import Level


def _two_floor_level():
    grid = [
        [TileType.FLOOR, TileType.FLOOR, TileType.WALL],
        [TileType.FLOOR, TileType.FLOOR, TileType.WALL],
    ]
    return Level(grid, (0, 0), (1, 1))


def test_player_blocked_by_wall():
    level = _two_floor_level()
    p = Player(0, 0)
    ms = MovementSystem()
    moved = ms.try_move_player(p, 2, 0, level)  # вне границ — стена
    assert moved is False
    assert p.position == (0, 0)


def test_player_picks_up_item_on_overlap():
    p = Player(2, 3)
    item = Item(2, 3)
    bus = EventBus()
    cs = CollisionSystem(bus)
    # игрок здоров — не вылечится, но кнопка должна засчитаться
    p.take_damage(1)
    cs.check_player_items(p, [item])
    assert item.alive is False
    assert p.buttons == 1


def test_aabb_basic():
    a = pygame.Rect(0, 0, 32, 32)
    b = pygame.Rect(20, 20, 32, 32)
    c = pygame.Rect(100, 100, 32, 32)
    assert CollisionSystem.aabb(a, b) is True
    assert CollisionSystem.aabb(a, c) is False
