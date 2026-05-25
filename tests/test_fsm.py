from src.entities.enemy import Enemy
from src.core.constants import PATROL, CHASE, RETURN


def test_starts_patrol():
    e = Enemy(0, 0, waypoints=[(0, 0), (3, 0)])
    assert e.state == PATROL


def test_patrol_to_chase_when_close():
    e = Enemy(0, 0, waypoints=[(0, 0), (3, 0)])
    e.update_fsm(2, 2)
    assert e.state == CHASE


def test_chase_to_return_when_far():
    e = Enemy(0, 0, waypoints=[(0, 0), (3, 0)])
    e.update_fsm(2, 2)
    e.update_fsm(20, 20)
    assert e.state == RETURN
