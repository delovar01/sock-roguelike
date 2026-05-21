import pytest

from src.entities.player import Player


def test_take_damage_reduces_hp():
    p = Player(0, 0)
    start = p.hp
    p.take_damage(1)
    assert p.hp == start - 1


def test_take_damage_does_not_go_below_zero():
    p = Player(0, 0)
    p.take_damage(1)
    p._invuln_timer = 0  # сбрасываем для теста
    p.take_damage(999)
    assert p.hp == 0
    assert p.is_dead()


def test_hp_is_read_only_property():
    p = Player(0, 0)
    with pytest.raises(AttributeError):
        p.hp = 100  # property без setter
