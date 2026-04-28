import pygame

from src.core.constants import (
    TILE_SIZE, TileType,
    WALL_COLOR, FLOOR_COLOR, EXIT_COLOR
)


class Level:
    """Уровень — двумерная сетка тайлов + позиция входа/выхода."""

    def __init__(self, grid, spawn, exit_pos):
        # grid — список списков TileType
        self.grid = grid
        self.spawn = spawn          # (tx, ty) старт игрока
        self.exit = exit_pos        # (tx, ty) выход
        self.height = len(grid)
        self.width = len(grid[0]) if self.height else 0

    def get_tile(self, tx, ty):
        # защита от выхода за пределы — снаружи стена
        if tx < 0 or ty < 0 or tx >= self.width or ty >= self.height:
            return TileType.WALL
        return self.grid[ty][tx]

    def is_walkable(self, tx, ty):
        t = self.get_tile(tx, ty)
        return t in (TileType.FLOOR, TileType.EXIT)

    def is_exit(self, tx, ty):
        return self.get_tile(tx, ty) == TileType.EXIT

    def draw(self, surface, camera):
        # рисуем только то что попадает в окно — простое отсечение
        start_x = max(0, camera.offset_x // TILE_SIZE)
        start_y = max(0, camera.offset_y // TILE_SIZE)
        end_x = min(self.width, (camera.offset_x + surface.get_width()) // TILE_SIZE + 1)
        end_y = min(self.height, (camera.offset_y + surface.get_height()) // TILE_SIZE + 1)

        for ty in range(start_y, end_y):
            for tx in range(start_x, end_x):
                tile = self.grid[ty][tx]
                px = tx * TILE_SIZE - camera.offset_x
                py = ty * TILE_SIZE - camera.offset_y
                if tile == TileType.WALL:
                    color = WALL_COLOR
                elif tile == TileType.EXIT:
                    color = EXIT_COLOR
                else:
                    color = FLOOR_COLOR
                pygame.draw.rect(surface, color, (px, py, TILE_SIZE, TILE_SIZE))
