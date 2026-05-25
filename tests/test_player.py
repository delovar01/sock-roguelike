from src.entities.player import Player


def test_take_damage():
    p = Player(0, 0)
    start = p.hp
    p.take_damage(1)
    assert p.hp == start - 1


def test_hp_not_below_zero():
    p = Player(0, 0)
    p.take_damage(1)
    p.invuln_timer = 0
    p.take_damage(999)
    assert p.hp == 0
    assert p.is_dead()


def test_heal_does_not_exceed_max():
    p = Player(0, 0)
    p.heal(100)  # уже на максимуме
    assert p.hp == 3
