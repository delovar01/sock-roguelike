class CollisionSystem:
    """Проверяет пересечения. Двигать ничего не двигает."""

    def __init__(self, event_bus):
        self.bus = event_bus

    @staticmethod
    def aabb(a, b):
        return a.colliderect(b)

    def check_player_items(self, player, items):
        """Если игрок встал на клетку предмета — подбираем."""
        for it in items:
            if not it.alive:
                continue
            if player.tx == it.tx and player.ty == it.ty:
                it.on_pickup(player)
                it.alive = False
                self.bus.emit("item_picked")

    def check_player_enemies(self, player, enemies):
        """Контакт с врагом = удар по игроку."""
        for enemy in enemies:
            if not enemy.alive:
                continue
            if player.tx == enemy.tx and player.ty == enemy.ty:
                if player.take_damage(1):
                    if player.is_dead():
                        self.bus.emit("player_died")
                return True
        return False

    def player_attack(self, player, enemies):
        """Игрок бьёт в 4 соседние клетки. Любой враг там — получает урон."""
        dirs = [(-1, 0), (1, 0), (0, -1), (0, 1)]
        hit = False
        for dx, dy in dirs:
            ax = player.tx + dx
            ay = player.ty + dy
            for enemy in enemies:
                if not enemy.alive:
                    continue
                if enemy.tx == ax and enemy.ty == ay:
                    enemy.take_damage(player.attack_damage)
                    hit = True
                    if not enemy.alive:
                        self.bus.emit("enemy_killed")
        if hit:
            self.bus.emit("player_attacked")
        return hit

    def bump_attack(self, player, dx, dy, enemies):
        """Если в клетке куда хочет шагнуть игрок стоит враг — бьём его.
        Возвращает True если был удар (тогда движение не происходит).
        """
        tx = player.tx + dx
        ty = player.ty + dy
        for enemy in enemies:
            if not enemy.alive:
                continue
            if enemy.tx == tx and enemy.ty == ty:
                enemy.take_damage(player.attack_damage)
                if not enemy.alive:
                    self.bus.emit("enemy_killed")
                self.bus.emit("player_attacked")
                return True
        return False
