"""ИИ первой версии — просто патрулирование."""


class AISystem:
    def update(self, enemies, player, level, dt, movement_system):
        for enemy in enemies:
            if not enemy.alive:
                continue
            if not enemy.can_step(dt):
                continue
            movement_system.step_enemy_to_waypoint(enemy, level)
