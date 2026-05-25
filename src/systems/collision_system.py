class CollisionSystem:
    """Проверки пересечений. Возвращает результат, ничего не двигает и звуки не играет."""

    def aabb(self, a, b):
        return a.colliderect(b)

    def check_player_items(self, player, items):
        """Игрок встал на предмет — подбираем. Возвращает список подобранных."""
        picked = []
        for it in items:
            if not it.alive:
                continue
            if player.tx == it.tx and player.ty == it.ty:
                it.on_pickup(player)
                it.alive = False
                picked.append(it)
        return picked

    def check_player_enemies(self, player, enemies):
        """Враг в той же клетке = удар по игроку. Возвращает True если ударили."""
        for enemy in enemies:
            if not enemy.alive:
                continue
            if player.tx == enemy.tx and player.ty == enemy.ty:
                player.take_damage(1)
                return True
        return False

    def player_attack(self, player, enemies):
        """Игрок бьёт в 4 соседние клетки.
        Возвращает (был_удар, убил_кого_то)."""
        dirs = [(-1, 0), (1, 0), (0, -1), (0, 1)]
        hit = False
        killed = False
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
                        killed = True
        return hit, killed

    def bump_attack(self, player, dx, dy, enemies):
        """Шагнул на врага = удар. Возвращает (был_удар, убил_ли)."""
        tx = player.tx + dx
        ty = player.ty + dy
        for enemy in enemies:
            if not enemy.alive:
                continue
            if enemy.tx == tx and enemy.ty == ty:
                enemy.take_damage(player.attack_damage)
                if not enemy.alive:
                    return True, True
                return True, False
        return False, False
