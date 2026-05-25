import pygame


# клавиши направления -> (dx, dy)
DIR_KEYS = {
    pygame.K_w: (0, -1),
    pygame.K_UP: (0, -1),
    pygame.K_s: (0, 1),
    pygame.K_DOWN: (0, 1),
    pygame.K_a: (-1, 0),
    pygame.K_LEFT: (-1, 0),
    pygame.K_d: (1, 0),
    pygame.K_RIGHT: (1, 0),
}

# задержка перед началом авто-повтора и период повторов
HOLD_DELAY = 0.18
HOLD_REPEAT = 0.08


class InputManager:
    """Управление с авто-повтором для клавиш движения.

    Если игрок зажал стрелку — первый шаг сразу, потом пауза HOLD_DELAY,
    потом шаги каждые HOLD_REPEAT секунд. Esc, пробел, F3 повтором не
    дёргаются — они срабатывают только по KEYDOWN в сценах.
    """

    def __init__(self):
        self.move_cmd = None
        self._last_dir = None
        self._timer = 0.0
        self._repeating = False

    def update(self, dt):
        keys = pygame.key.get_pressed()

        # ищем какое направление сейчас зажато
        current = None
        for key, direction in DIR_KEYS.items():
            if keys[key]:
                current = direction
                break

        # сначала всегда сбрасываем команду
        self.move_cmd = None

        if current is None:
            # ничего не зажато — обнуляем состояние
            self._last_dir = None
            self._timer = 0.0
            self._repeating = False
            return

        if current != self._last_dir:
            # новое направление — сразу один шаг
            self.move_cmd = current
            self._last_dir = current
            self._timer = 0.0
            self._repeating = False
            return

        # то же направление продолжается
        self._timer += dt
        if not self._repeating:
            if self._timer >= HOLD_DELAY:
                self._repeating = True
                self._timer = 0.0
                self.move_cmd = current
        else:
            if self._timer >= HOLD_REPEAT:
                self._timer = 0.0
                self.move_cmd = current
