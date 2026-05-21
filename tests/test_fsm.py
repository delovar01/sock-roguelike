from src.entities.enemy import Enemy
from src.core.constants import EnemyState


def test_initial_state_is_patrol():
    e = Enemy(0, 0, waypoints=[(0, 0), (3, 0)])
    assert e.state == EnemyState.PATROL


def test_patrol_to_chase_when_player_in_radius():
    e = Enemy(0, 0, waypoints=[(0, 0), (3, 0)])
    # игрок в радиусе DETECT_RADIUS=5
    e.update_fsm(player_tx=2, player_ty=2)
    assert e.state == EnemyState.CHASE


def test_chase_to_return_when_player_far():
    e = Enemy(0, 0, waypoints=[(0, 0), (3, 0)])
    e.update_fsm(2, 2)
    assert e.state == EnemyState.CHASE
    # игрок ушёл за LOSE_RADIUS=8
    e.update_fsm(20, 20)
    assert e.state == EnemyState.RETURN
