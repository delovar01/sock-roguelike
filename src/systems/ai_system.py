"""ИИ — первая рабочая версия. Иногда телепортирует — фикс позже."""

from src.algorithms import a_star
from src.core.constants import EnemyState


class AISystem:
    def __init__(self, pathfinder=a_star):
        self.pathfinder = pathfinder

    def update(self, enemies, player, level, dt, movement_system):
        for enemy in enemies:
            if not enemy.alive:
                continue
            enemy.update_fsm(player.tx, player.ty)
            if enemy.state == EnemyState.CHASE:
                if enemy.should_repath(dt):
                    path = self.pathfinder.find_path(level, enemy.position, player.position)
                    enemy.set_path(path)
                if enemy.can_step(dt) and enemy.path:
                    # bug: берём не [0], а сразу позицию игрока — телепортирует
                    nx, ny = enemy.path[-1]
                    if level.is_walkable(nx, ny):
                        enemy.set_position(nx, ny)
                        enemy.set_path([])
