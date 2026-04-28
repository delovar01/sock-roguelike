from enum import Enum
from pathlib import Path

# окно
SCREEN_WIDTH = 960
SCREEN_HEIGHT = 704
FPS = 60
WINDOW_TITLE = "Носок-одиночка"

# тайлы
TILE_SIZE = 32
MAP_WIDTH = 40
MAP_HEIGHT = 30

# игрок
PLAYER_SPEED = 4
PLAYER_MAX_HP = 3
PLAYER_COLOR = (240, 240, 240)

# враг
ENEMY_SPEED = 2
ENEMY_COLOR = (130, 80, 50)
DETECT_RADIUS = 5
LOSE_RADIUS = 8
AI_REPATH_FRAMES = 15

# предметы
ITEM_COLOR = (230, 190, 60)

# уровень и BSP
LEVELS_COUNT = 3
BSP_MIN_LEAF_SIZE = 7
BSP_MAX_DEPTH = 5
ROOM_MIN_SIZE = 4
ROOM_PADDING = 1

# тайлы цвета
WALL_COLOR = (110, 115, 125)
FLOOR_COLOR = (140, 180, 210)
EXIT_COLOR = (255, 230, 240)
BG_COLOR = (25, 30, 40)

# UI
HUD_COLOR = (255, 255, 255)
FONT_SIZE = 22

# пути
ROOT_DIR = Path(__file__).resolve().parent.parent.parent
ASSETS_DIR = ROOT_DIR / "assets"
SAVE_DIR = ROOT_DIR / "saves"
SAVE_FILE = SAVE_DIR / "slot1.json"
STORY_FILE = ASSETS_DIR / "story" / "intro.txt"


class TileType(Enum):
    WALL = 0
    FLOOR = 1
    EXIT = 2


class EnemyState(Enum):
    PATROL = "patrol"
    CHASE = "chase"
    RETURN = "return"


class SceneId(Enum):
    MENU = "menu"
    GAME = "game"
    DEATH = "death"
    WIN = "win"
