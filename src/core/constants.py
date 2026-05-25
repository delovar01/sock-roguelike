import os

# окно
SCREEN_WIDTH = 960
SCREEN_HEIGHT = 704
FPS = 60
WINDOW_TITLE = "Носок-одиночка"

# тайлы
TILE_SIZE = 32
MAP_WIDTH = 50
MAP_HEIGHT = 36

# типы тайлов
WALL = 0
FLOOR = 1
EXIT = 2

# состояния врага
PATROL = "patrol"
CHASE = "chase"
RETURN = "return"

# id сцен
MENU = "menu"
GAME = "game"
DEATH = "death"
WIN = "win"

# игрок
PLAYER_MAX_HP = 3
PLAYER_COLOR = (240, 240, 240)
PLAYER_BASE_DAMAGE = 1

# враги
ENEMY_COLOR = (130, 80, 50)
SPIDER_COLOR = (200, 90, 200)
DETECT_RADIUS = 5
LOSE_RADIUS = 8
SPIDER_DETECT_RADIUS = 3
SPIDER_LOSE_RADIUS = 6
MOTH_HP = 2
SPIDER_HP = 1

# предметы
BUTTON_COLOR = (230, 190, 60)
NEEDLE_COLOR = (200, 200, 230)
KEY_COLOR = (230, 130, 50)

# очки
SCORE_BUTTON = 10
SCORE_NEEDLE = 30
SCORE_KEY = 20
SCORE_KILL = 50

# уровень и BSP
LEVELS_COUNT = 5
BSP_MIN_LEAF_SIZE = 7
BSP_MAX_DEPTH = 6
ROOM_MIN_SIZE = 4
ROOM_PADDING = 1

# цвета мира и UI
WALL_COLOR = (110, 115, 125)
FLOOR_COLOR = (140, 180, 210)
EXIT_COLOR = (255, 230, 240)
BG_COLOR = (25, 30, 40)
HUD_COLOR = (255, 255, 255)

# подсветка факелом
LIGHT_RADIUS = 110
LIGHT_FADE = 50
LIGHT_DARKNESS = 220

# пути к ресурсам
ROOT_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
ASSETS_DIR = os.path.join(ROOT_DIR, "assets")
SAVE_DIR = os.path.join(ROOT_DIR, "saves")
SAVE_FILE = os.path.join(SAVE_DIR, "slot1.json")
STORY_FILE = os.path.join(ASSETS_DIR, "story", "intro.txt")
