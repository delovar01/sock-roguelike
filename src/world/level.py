import pygame

from src.core.constants import (
    TILE_SIZE, WALL, FLOOR, EXIT,
    WALL_COLOR, FLOOR_COLOR, EXIT_COLOR,
)


class Level:
    """Уровень — двумерная сетка тайлов."""

    def __init__(self, grid, spawn, exit_pos):
        self.grid = grid
        self.spawn = spawn
        self.exit = exit_pos
        self.height = len(grid)
        self.width = len(grid[0]) if self.height else 0

    def get_tile(self, tx, ty):
        if tx < 0 or ty < 0 or tx >= self.width or ty >= self.height:
            return WALL
        return self.grid[ty][tx]

    def is_walkable(self, tx, ty):
        t = self.get_tile(tx, ty)
        return t == FLOOR or t == EXIT

    def is_exit(self, tx, ty):
        return self.get_tile(tx, ty) == EXIT

    def draw(self, surface, camera):
        start_x = max(0, camera.offset_x // TILE_SIZE)
        start_y = max(0, camera.offset_y // TILE_SIZE)
        end_x = min(self.width, (camera.offset_x + surface.get_width()) // TILE_SIZE + 1)
        end_y = min(self.height, (camera.offset_y + surface.get_height()) // TILE_SIZE + 1)
        for ty in range(start_y, end_y):
            for tx in range(start_x, end_x):
                tile = self.grid[ty][tx]
                px = tx * TILE_SIZE - camera.offset_x
                py = ty * TILE_SIZE - camera.offset_y
                if tile == WALL:
                    color = WALL_COLOR
                elif tile == EXIT:
                    color = EXIT_COLOR
                else:
                    color = FLOOR_COLOR
                pygame.draw.rect(surface, color, (px, py, TILE_SIZE, TILE_SIZE))
