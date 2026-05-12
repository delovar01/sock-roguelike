"""Логика врагов — обновление FSM и поиск пути.

Зависит от абстракции AStar через параметр pathfinder, что позволяет
подменить алгоритм поиска (Dependency Inversion).
"""

from src.core.constants import EnemyState


class AISystem:
    def __init__(self, pathfinder):
        # pathfinder — модуль или объект с функцией find_path(level, start, goal)
        self.pathfinder = pathfinder

    def update(self, enemies, player, level, dt, movement_system):
        for enemy in enemies:
            if not enemy.alive:
                continue
            enemy.update_fsm(player.tx, player.ty)

            if enemy.state == EnemyState.CHASE:
                if enemy.should_repath(dt):
                    path = self.pathfinder.find_path(
                        level, enemy.position, player.position
                    )
                    enemy.set_path(path)

            if not enemy.can_step(dt):
                continue

            if enemy.state == EnemyState.PATROL:
                movement_system.step_enemy_to_waypoint(enemy, level)
            elif enemy.state == EnemyState.CHASE:
                if enemy.path:
                    movement_system.step_enemy_towards(
                        enemy, player.tx, player.ty, level
                    )
            elif enemy.state == EnemyState.RETURN:
                movement_system.step_enemy_to_waypoint(enemy, level)
