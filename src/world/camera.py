from src.core.constants import TILE_SIZE


class Camera:
    """Простая 2D-камера со смещением.

    Следует за целью, но не выходит за края уровня (clamp).
    """

    def __init__(self, screen_width, screen_height, level_width, level_height):
        self.screen_w = screen_width
        self.screen_h = screen_height
        self.world_w = level_width * TILE_SIZE
        self.world_h = level_height * TILE_SIZE
        self.offset_x = 0
        self.offset_y = 0

    def follow(self, target_tx, target_ty):
        # цель в центре экрана
        cx = target_tx * TILE_SIZE + TILE_SIZE // 2
        cy = target_ty * TILE_SIZE + TILE_SIZE // 2
        self.offset_x = cx - self.screen_w // 2
        self.offset_y = cy - self.screen_h // 2
        self._clamp()

    def _clamp(self):
        max_x = max(0, self.world_w - self.screen_w)
        max_y = max(0, self.world_h - self.screen_h)
        if self.offset_x < 0:
            self.offset_x = 0
        if self.offset_y < 0:
            self.offset_y = 0
        if self.offset_x > max_x:
            self.offset_x = max_x
        if self.offset_y > max_y:
            self.offset_y = max_y
