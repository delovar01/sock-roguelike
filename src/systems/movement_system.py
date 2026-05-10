class MovementSystem:
    """Двигает игрока и врагов на одну клетку. Без поиска пути."""

    def try_move_player(self, player, dx, dy, level):
        new_tx = player.tx + dx
        new_ty = player.ty + dy
        if level.is_walkable(new_tx, new_ty):
            player.set_position(new_tx, new_ty)
            return True
        return False

    def step_enemy_to_waypoint(self, enemy, level):
        wp = enemy.current_waypoint()
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
