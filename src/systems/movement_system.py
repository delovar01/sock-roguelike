class MovementSystem:
    """Двигает игрока на одну клетку по команде из InputManager.

    Враги двигаются через AISystem — отдельная логика.
    """

    def try_move_player(self, player, dx, dy, level):
        new_tx = player.tx + dx
        new_ty = player.ty + dy
        if level.is_walkable(new_tx, new_ty):
            player.set_position(new_tx, new_ty)
            return True
        return False

    def step_enemy_towards(self, enemy, target_tx, target_ty, level):
        # делаем один шаг по path[0] если есть, или к target напрямую
        path = enemy.path
        if path:
            next_step = path[0]
            if level.is_walkable(*next_step):
                enemy.set_position(*next_step)
                enemy.set_path(path[1:])
                return True
        return False

    def step_enemy_to_waypoint(self, enemy, level):
        wp = enemy.current_waypoint()
        # тупой шаг к точке — без поиска пути
        dx = 0
        dy = 0
        if enemy.tx < wp[0]:
            dx = 1
        elif enemy.tx > wp[0]:
            dx = -1
        elif enemy.ty < wp[1]:
            dy = 1
        elif enemy.ty > wp[1]:
            dy = -1
        if dx == 0 and dy == 0:
            enemy.advance_waypoint()
            return False
        nx, ny = enemy.tx + dx, enemy.ty + dy
        if level.is_walkable(nx, ny):
            enemy.set_position(nx, ny)
            return True
        return False
