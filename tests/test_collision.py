from src.entities.player import Player
from src.entities.item import Button, Needle
from src.entities.enemy import Enemy
from src.systems.movement_system import MovementSystem
from src.systems.collision_system import CollisionSystem
from src.core.constants import FLOOR, WALL
from src.world.level import Level


def test_player_blocked_by_wall():
    grid = [[FLOOR, FLOOR, WALL]]
    level = Level(grid, (0, 0), (1, 0))
    p = Player(0, 0)
    ms = MovementSystem()
    moved = ms.try_move_player(p, 5, 0, level)  # сильно вне границ
    assert moved is False
    assert (p.tx, p.ty) == (0, 0)


def test_button_pickup_heals():
    p = Player(2, 2)
    p.take_damage(1)
    start_hp = p.hp
    btn = Button(2, 2)
    cs = CollisionSystem()
    cs.check_player_items(p, [btn])
    assert btn.alive is False
    assert p.hp == start_hp + 1


def test_needle_increases_damage():
    p = Player(0, 0)
    n = Needle(0, 0)
    cs = CollisionSystem()
    start = p.attack_damage
    cs.check_player_items(p, [n])
    assert p.attack_damage == start + 1


def test_bump_attack():
    p = Player(5, 5)
    e = Enemy(6, 5, waypoints=[(6, 5)], hp=1)
    cs = CollisionSystem()
    hit, killed = cs.bump_attack(p, 1, 0, [e])
    assert hit is True
    assert killed is True
    assert (p.tx, p.ty) == (5, 5)
