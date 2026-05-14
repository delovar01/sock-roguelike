class CollisionSystem:
    """AABB-проверки и обработка пересечений.

    Не двигает никого — только проверяет и эмитит события.
    """

    def __init__(self, event_bus):
        self.bus = event_bus

    @staticmethod
    def aabb(a, b):
        # два rect пересекаются
        return a.colliderect(b)

    def check_player_items(self, player, items):
        picked = []
        for it in items:
            if not it.alive:
                continue
            if player.tx == it.tx and player.ty == it.ty:
                if player.heal(1):
                    it.alive = False
                    player.add_button()
                    self.bus.emit("item_picked")
                    picked.append(it)
                else:
                    # уже полный — тоже считаем подбор как очко
                    it.alive = False
                    player.add_button()
                    self.bus.emit("item_picked")
                    picked.append(it)
        return picked

    def check_player_enemies(self, player, enemies):
        for enemy in enemies:
            if not enemy.alive:
                continue
            if player.tx == enemy.tx and player.ty == enemy.ty:
                if player.take_damage(1):
                    if player.is_dead():
                        self.bus.emit("player_died")
                return True
        return False
