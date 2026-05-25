import pygame
import random

from src.scenes.base_scene import BaseScene
from src.core.constants import (
    SCREEN_WIDTH, SCREEN_HEIGHT, MAP_WIDTH, MAP_HEIGHT,
    LEVELS_COUNT, SceneId, TileType, HUD_COLOR
)
from src.algorithms import bsp_dungeon, a_star
from src.entities.player import Player
from src.entities.enemy import Enemy
from src.entities.item import Item
from src.world.level import Level
from src.world.camera import Camera
from src.systems.movement_system import MovementSystem
from src.systems.collision_system import CollisionSystem
from src.systems.ai_system import AISystem
from src.systems.render_system import RenderSystem
from src.ui.hud import Hud
from src.persistence.save_manager import save_game, load_game


def _spawn_enemies_and_items(rooms, centers, spawn, exit_pos, rng, level_num):
    """Расставляем врагов и предметы в комнатах кроме стартовой."""
    enemies = []
    items = []
    if len(rooms) < 2:
        return enemies, items
    # на каждом уровне врагов и пуговиц чуть больше
    # TODO: можно ещё типы врагов добавить, паука например
    enemy_count = min(1 + level_num, len(rooms) - 1)
    item_count = min(2 + level_num, len(rooms) - 1)

    skip_centers = {spawn, exit_pos}
    available = [c for c in centers if c not in skip_centers]
    rng.shuffle(available)

    for c in available[:enemy_count]:
        # делаем простой waypoint-маршрут — две точки около центра
        room = _room_for_center(rooms, c)
        wps = _make_waypoints(room)
        enemies.append(Enemy(c[0], c[1], wps))

    for c in available[enemy_count:enemy_count + item_count]:
        items.append(Item(c[0], c[1]))

    return enemies, items


def _room_for_center(rooms, center):
    for r in rooms:
        if r[0] + r[2] // 2 == center[0] and r[1] + r[3] // 2 == center[1]:
            return r
    return rooms[0]


def _make_waypoints(room):
    rx, ry, rw, rh = room
    if rw <= 2 or rh <= 2:
        return [(rx + rw // 2, ry + rh // 2)]
    a = (rx + 1, ry + 1)
    b = (rx + rw - 2, ry + rh - 2)
    return [a, b]


class GameScene(BaseScene):
    def __init__(self, game, level_num=1, load_save=False, saved_state=None):
        super().__init__(game)
        self.movement = MovementSystem()
        self.collisions = CollisionSystem(game.event_bus)
        self.ai = AISystem(pathfinder=a_star)
        self.render_sys = RenderSystem()
        self.hud = Hud(game.resources)

        # подписки на события
        game.event_bus.subscribe("item_picked", self._on_item_picked)
        game.event_bus.subscribe("player_died", self._on_player_died)
        game.event_bus.subscribe("level_completed", self._on_level_completed)
        self.paused = False

        if load_save:
            data = load_game()
            if data is None:
                # сохранения нет — стартуем новую
                self.level_num = 1
                self._init_level(seed=12345, restore=None)
            else:
                self.level_num = data["level_num"]
                self._init_level(seed=data["seed"],
                                 restore={"hp": data["hp"],
                                          "buttons": data["buttons"]})
        else:
            self.level_num = level_num
            self._init_level(seed=_seed_for_level(level_num), restore=None)

    def _init_level(self, seed, restore):
        rng = random.Random(seed + 7)  # отдельный rng для размещения
        result = bsp_dungeon.generate_with_rooms(MAP_WIDTH, MAP_HEIGHT, seed)
        grid, spawn, exit_pos, rooms, centers = result
        self.level = Level(grid, spawn, exit_pos)
        self.player = Player(*spawn)
        if restore is not None:
            self.player.set_state(restore["hp"], restore["buttons"])
        self.camera = Camera(SCREEN_WIDTH, SCREEN_HEIGHT,
                             self.level.width, self.level.height)
        self.camera.follow(self.player.tx, self.player.ty)
        self.enemies, self.items = _spawn_enemies_and_items(
            rooms, centers, spawn, exit_pos, rng, self.level_num
        )
        self.seed = seed
        self._save_on_next_step = True  # авто-сейв на старте уровня
        self._game_over = False

    def _on_item_picked(self):
        self.game.resources.play_sound("pickup.wav")

    def _on_player_died(self):
        self.game.resources.play_sound("death.wav")
        self._game_over = True
        self.game.change_scene(SceneId.DEATH)

    def _on_level_completed(self):
        self.game.resources.play_sound("win.wav")
        if self.level_num >= LEVELS_COUNT:
            self.game.change_scene(SceneId.WIN)
        else:
            self.level_num += 1
            self._init_level(seed=_seed_for_level(self.level_num), restore=None)

    def handle_event(self, event):
        if event.type != pygame.KEYDOWN:
            return
        if event.key == pygame.K_ESCAPE:
            # на паузу или с паузы
            self.paused = not self.paused
            if self.paused:
                # сохраняем сразу когда зашли в паузу
                save_game(self.level_num, self.seed, self.player.hp, self.player.buttons)
        elif event.key == pygame.K_F3:
            self.render_sys.toggle_debug()
        elif self.paused and event.key == pygame.K_q:
            # из паузы можно выйти в меню
            self.game.change_scene(SceneId.MENU)
        elif self.paused and event.key == pygame.K_MINUS:
            self.game.resources.change_music_volume(-0.1)
        elif self.paused and event.key in (pygame.K_EQUALS, pygame.K_PLUS):
            self.game.resources.change_music_volume(0.1)

    def update(self, dt):
        if self._game_over or self.paused:
            return

        # порядок шагов в кадре — как в методичке
        # Input -> Movement -> Collision -> AI -> Logic

        # 1. Input — что нажал игрок в этом кадре
        cmd = self.game.input_manager.move_cmd
        if cmd is not None:
            dx, dy = cmd
            # 2. Movement игрока + 3. Collision сразу же
            moved = self.movement.try_move_player(self.player, dx, dy, self.level)
            if moved:
                self._after_player_move()

        # авто-сейв на старте уровня
        if self._save_on_next_step:
            save_game(self.level_num, self.seed, self.player.hp, self.player.buttons)
            self._save_on_next_step = False

        # 4. AI — обновление врагов (вкл. их Movement)
        self.ai.update(self.enemies, self.player, self.level, dt, self.movement)
        # 5. Collision после хода врагов
        self.collisions.check_player_enemies(self.player, self.enemies)
        # 6. Logic — таймер неуязвимости игрока
        self.player.update(dt, None)

    def _after_player_move(self):
        # подбор предметов
        self.collisions.check_player_items(self.player, self.items)
        # пересечение с врагом сразу же
        self.collisions.check_player_enemies(self.player, self.enemies)
        # достигли выхода?
        if self.level.is_exit(self.player.tx, self.player.ty):
            self.game.event_bus.emit("level_completed")
        self.camera.follow(self.player.tx, self.player.ty)

    def draw(self, surface):
        all_entities = list(self.items) + list(self.enemies) + [self.player]
        self.render_sys.draw(surface, self.level, all_entities, self.camera)
        fps = self.game.clock.get_fps()
        self.render_sys.draw_debug(surface, self.enemies, self.camera, fps)
        self.hud.draw(surface, self.player, self.level_num)
        if self.paused:
            self._draw_pause(surface)

    def _draw_pause(self, surface):
        # затемнение
        overlay = pygame.Surface((surface.get_width(), surface.get_height()))
        overlay.set_alpha(170)
        overlay.fill((0, 0, 0))
        surface.blit(overlay, (0, 0))
        font_big = self.game.resources.get_font(48)
        font = self.game.resources.get_font(22)
        cx = surface.get_width() // 2
        cy = surface.get_height() // 2
        title = font_big.render("Пауза", True, (255, 255, 255))
        surface.blit(title, title.get_rect(center=(cx, cy - 80)))
        lines = [
            "Esc — продолжить",
            "Q — в главное меню (сохранится)",
            "+ / - — громкость музыки",
        ]
        for i, ln in enumerate(lines):
            s = font.render(ln, True, (220, 220, 220))
            surface.blit(s, s.get_rect(center=(cx, cy - 10 + i * 28)))


def _seed_for_level(level_num):
    base = 1000
    return base + level_num * 17
