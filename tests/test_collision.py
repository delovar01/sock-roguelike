import pygame

from src.entities.player import Player
from src.entities.item import Button, Needle
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


def test_button_pickup_heals_and_counts():
    p = Player(2, 3)
    btn = Button(2, 3)
    bus = EventBus()
    cs = CollisionSystem(bus)
    # сначала ранится, потом подбирает пуговицу
    p.take_damage(1)
    start_hp = p.hp
    cs.check_player_items(p, [btn])
    assert btn.alive is False
    assert p.buttons == 1
    assert p.hp == start_hp + 1


def test_needle_pickup_increases_damage():
    p = Player(0, 0)
    n = Needle(0, 0)
    bus = EventBus()
    cs = CollisionSystem(bus)
    start = p.attack_damage
    cs.check_player_items(p, [n])
    assert n.alive is False
    assert p.attack_damage == start + 1


def test_player_attack_kills_enemy():
    p = Player(5, 5)
    e = Enemy(6, 5, waypoints=[(6, 5)], hp=1)
    bus = EventBus()
    cs = CollisionSystem(bus)
    hit = cs.player_attack(p, [e])
    assert hit is True
    assert e.alive is False


def test_bump_attack_hits_instead_of_moving():
    p = Player(5, 5)
    # враг прямо справа
    e = Enemy(6, 5, waypoints=[(6, 5)], hp=2)
    bus = EventBus()
    cs = CollisionSystem(bus)
    hit = cs.bump_attack(p, dx=1, dy=0, enemies=[e])
    assert hit is True
    assert e.hp == 1
    # игрок не сдвинулся
    assert p.position == (5, 5)


def test_aabb_basic():
    a = pygame.Rect(0, 0, 32, 32)
    b = pygame.Rect(20, 20, 32, 32)
    c = pygame.Rect(100, 100, 32, 32)
    assert CollisionSystem.aabb(a, b) is True
    assert CollisionSystem.aabb(a, c) is False
