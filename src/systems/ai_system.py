"""Логика врагов — обновляем автомат и иногда зовём поиск пути."""

from src.core.constants import EnemyState


class AISystem:
    def __init__(self, pathfinder):
        # pathfinder — модуль с функцией find_path(level, start, goal)
        self.pathfinder = pathfinder

    def update(self, enemies, player, level, dt, movement_system):
        for enemy in enemies:
            if not enemy.alive:
                continue
            # 1. обновляем автомат состояния
            enemy.update_fsm(player.tx, player.ty)

            # 2. в Chase раз в 0.25с зовём A*
            if enemy.state == EnemyState.CHASE:
                if enemy.should_repath(dt):
                    path = self.pathfinder.find_path(
                        level, enemy.position, player.position
                    )
                    enemy.set_path(path)

            # 3. двигаем врага не чаще чем раз в move_period
            if not enemy.can_step(dt):
                continue

            # FIXME: если state=Chase, но path пустой (игрок за стеной без обхода),
            # враг просто стоит. По-хорошему перевести в Return, но пока работает
            if enemy.state == EnemyState.PATROL:
                movement_system.step_enemy_to_waypoint(enemy, level)
            elif enemy.state == EnemyState.CHASE:
                if enemy.path:
                    movement_system.step_enemy_towards(
                        enemy, player.tx, player.ty, level
                    )
            elif enemy.state == EnemyState.RETURN:
                movement_system.step_enemy_to_waypoint(enemy, level)
