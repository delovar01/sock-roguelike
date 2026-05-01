import pygame

# отображение клавиш в направления (dx, dy) по тайлам
KEY_DIRS = {
    pygame.K_w: (0, -1),
    pygame.K_UP: (0, -1),
    pygame.K_s: (0, 1),
    pygame.K_DOWN: (0, 1),
    pygame.K_a: (-1, 0),
    pygame.K_LEFT: (-1, 0),
    pygame.K_d: (1, 0),
    pygame.K_RIGHT: (1, 0),
}


class InputManager:
    """Превращает события клавиатуры в простые команды."""

    def __init__(self):
        self.move_cmd = None  # (dx, dy) или None
        self.toggle_debug = False
        self.escape = False
        self.confirm = False

    def reset_frame(self):
        self.move_cmd = None
        self.toggle_debug = False
        self.escape = False
        self.confirm = False

    def handle(self, event):
        if event.type != pygame.KEYDOWN:
            return
        if event.key in KEY_DIRS:
            self.move_cmd = KEY_DIRS[event.key]
        elif event.key == pygame.K_F3:
            self.toggle_debug = True
        elif event.key == pygame.K_ESCAPE:
            self.escape = True
        elif event.key in (pygame.K_RETURN, pygame.K_SPACE):
            self.confirm = True
