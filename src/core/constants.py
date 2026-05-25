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

# враги
ENEMY_SPEED = 2
ENEMY_COLOR = (130, 80, 50)        # моль
SPIDER_COLOR = (200, 90, 200)      # паук
DETECT_RADIUS = 5                   # клеток
LOSE_RADIUS = 8                     # для гистерезиса
SPIDER_DETECT_RADIUS = 3            # паук ближе видит
SPIDER_LOSE_RADIUS = 6
MOTH_HP = 2
SPIDER_HP = 1

# предметы
BUTTON_COLOR = (230, 190, 60)      # пуговица: +1 HP
NEEDLE_COLOR = (200, 200, 230)     # иголка: +1 урона
KEY_COLOR = (230, 130, 50)         # ключ: открывает выход
ITEM_COLOR = BUTTON_COLOR           # для обратной совместимости

# атака игрока
PLAYER_BASE_DAMAGE = 1

# очки
SCORE_BUTTON = 10
SCORE_NEEDLE = 30
SCORE_KEY = 20
SCORE_KILL = 50

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
