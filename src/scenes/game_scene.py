import pygame
import random

from src.scenes.base_scene import BaseScene
from src.core.constants import (
    SCREEN_WIDTH, SCREEN_HEIGHT, MAP_WIDTH, MAP_HEIGHT,
    LEVELS_COUNT, SceneId, SCORE_KILL
)
from src.algorithms import bsp_dungeon, a_star
from src.entities.player import Player
from src.entities.enemy import Enemy, Spider
from src.entities.item import Button, Needle, Key
from src.world.level import Level
from src.world.camera import Camera
from src.systems.movement_system import MovementSystem
from src.systems.collision_system import CollisionSystem
from src.systems.ai_system import AISystem
from src.systems.render_system import RenderSystem
from src.ui.hud import Hud
from src.persistence.save_manager import save_game, load_game


def _spawn_enemies_and_items(rooms, centers, spawn, exit_pos, rng, level_num):
    """Расставляем врагов и предметы. На каждом уровне обязательно один Key."""
    enemies = []
    items = []
    if len(rooms) < 2:
        return enemies, items

    # с уровнем растёт число врагов и их HP
    enemy_count = min(2 + level_num, len(rooms) - 1)
    # предметов меньше чем раньше — иначе слишком легко лечиться
    item_count = min(2 + level_num // 2, len(rooms) - 1)

    skip_centers = {spawn, exit_pos}
    available = [c for c in centers if c not in skip_centers]
    rng.shuffle(available)

    # +1 HP врагам за каждые 2 уровня. На 5-м моль уже с 4 HP
    moth_hp = 2 + (level_num - 1) // 2
    spider_hp = 1 + (level_num - 1) // 2

    # враги: на 1-м уровне только моли, со 2-го появляются пауки
    enemy_slots = available[:enemy_count]
    for i, c in enumerate(enemy_slots):
        room = _room_for_center(rooms, c)
        wps = _make_waypoints(room)
        # каждый третий враг (начиная с уровня 2) — паук
        if level_num >= 2 and i % 3 == 1:
            sp = Spider(c[0], c[1], wps)
            sp.hp = spider_hp
            enemies.append(sp)
        else:
            enemies.append(Enemy(c[0], c[1], wps, hp=moth_hp))

    # предметы: первый слот всегда ключ
    item_slots = available[enemy_count:enemy_count + item_count]
    for i, c in enumerate(item_slots):
        if i == 0:
            items.append(Key(c[0], c[1]))
        elif level_num >= 2 and i == 1:
            items.append(Needle(c[0], c[1]))
        else:
            items.append(Button(c[0], c[1]))

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
        game.event_bus.subscribe("player_attacked", self._on_player_attacked)
        game.event_bus.subscribe("enemy_killed", self._on_enemy_killed)
        game.event_bus.subscribe("player_died", self._on_player_died)
        game.event_bus.subscribe("level_completed", self._on_level_completed)
        self.paused = False

        # сообщение игроку (например "нужен ключ") и таймер его показа
        self.message = ""
        self.message_timer = 0.0

        # секундомер всей игры — копится за все уровни
        self.elapsed_time = 0.0

        if load_save:
            data = load_game()
            if data is None:
                self.level_num = 1
                self._init_level(seed=12345, restore=None)
            else:
                self.level_num = data["level_num"]
                self.elapsed_time = data.get("time", 0.0)
                self._init_level(
                    seed=data["seed"],
                    restore={
                        "hp": data["hp"],
                        "buttons": data["buttons"],
                        "attack": data.get("attack", 1),
                        "score": data.get("score", 0),
                        "kills": data.get("kills", 0),
                    },
                )
        else:
            self.level_num = level_num
            self._init_level(seed=_seed_for_level(level_num), restore=None)

    def _init_level(self, seed, restore):
        rng = random.Random(seed + 7)
        grid, spawn, exit_pos, rooms, centers = bsp_dungeon.generate(
            MAP_WIDTH, MAP_HEIGHT, seed
        )
        self.level = Level(grid, spawn, exit_pos)
        self.player = Player(*spawn)
        if restore is not None:
            self.player.set_state(
                restore["hp"], restore["buttons"],
                restore.get("attack", 1),
                restore.get("score", 0),
                restore.get("kills", 0),
            )
        self.camera = Camera(SCREEN_WIDTH, SCREEN_HEIGHT,
                             self.level.width, self.level.height)
        self.camera.follow(self.player.tx, self.player.ty)
        self.enemies, self.items = _spawn_enemies_and_items(
            rooms, centers, spawn, exit_pos, rng, self.level_num
        )
        self.seed = seed
        self._save_on_next_step = True
        self._game_over = False

    def _show_message(self, text, seconds=1.5):
        self.message = text
        self.message_timer = seconds

    def _on_item_picked(self):
        self.game.resources.play_sound("pickup.wav")

    def _on_player_attacked(self):
        self.game.resources.play_sound("hit.wav")

    def _on_enemy_killed(self):
        self.game.resources.play_sound("enemy_die.wav")
        self.player.add_kill()
        self.player.add_score(SCORE_KILL)

    def _on_player_died(self):
        self.game.resources.play_sound("death.wav")
        self._game_over = True
        self.game.change_scene(SceneId.DEATH)

    def _on_level_completed(self):
        self.game.resources.play_sound("win.wav")
        if self.level_num >= LEVELS_COUNT:
            # итоговая статистика для WinScene
            stats = {
                "score": self.player.score,
                "kills": self.player.kills,
                "buttons": self.player.buttons,
                "time": self.elapsed_time,
            }
            self.game.change_scene(SceneId.WIN, stats=stats)
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
                self._save()
        elif event.key == pygame.K_F3:
            self.render_sys.toggle_debug()
        elif event.key == pygame.K_SPACE:
            if not self.paused and not self._game_over:
                self.collisions.player_attack(self.player, self.enemies)
        elif self.paused and event.key == pygame.K_q:
            self.game.change_scene(SceneId.MENU)
        elif self.paused and event.key == pygame.K_MINUS:
            self.game.resources.change_music_volume(-0.1)
        elif self.paused and event.key in (pygame.K_EQUALS, pygame.K_PLUS):
            self.game.resources.change_music_volume(0.1)

    def update(self, dt):
        if self._game_over or self.paused:
            return

        # копим время уровня и таймер сообщения
        self.elapsed_time += dt
        if self.message_timer > 0:
            self.message_timer -= dt

        # порядок шагов в кадре — как в методичке
        # Input -> Movement -> Collision -> AI -> Logic

        # 1. Input — что нажал игрок
        cmd = self.game.input_manager.move_cmd
        if cmd is not None:
            dx, dy = cmd
            # если в той клетке стоит враг — бьём его (bump attack)
            attacked = self.collisions.bump_attack(self.player, dx, dy, self.enemies)
            if not attacked:
                # 2. Movement игрока + 3. Collision
                moved = self.movement.try_move_player(self.player, dx, dy, self.level)
                if moved:
                    self._after_player_move()

        if self._save_on_next_step:
            self._save()
            self._save_on_next_step = False

        # 4. AI и движение врагов
        self.ai.update(self.enemies, self.player, self.level, dt, self.movement)
        # 5. Collision после хода врагов
        self.collisions.check_player_enemies(self.player, self.enemies)
        # 6. Logic — таймер неуязвимости
        self.player.update(dt, None)

    def _save(self):
        save_game(
            level_num=self.level_num,
            seed=self.seed,
            hp=self.player.hp,
            buttons=self.player.buttons,
            attack=self.player.attack_damage,
            score=self.player.score,
            kills=self.player.kills,
            time=self.elapsed_time,
        )

    def _after_player_move(self):
        # подбор предметов
        self.collisions.check_player_items(self.player, self.items)
        # пересечение с врагом сразу же
        self.collisions.check_player_enemies(self.player, self.enemies)
        # достигли выхода?
        if self.level.is_exit(self.player.tx, self.player.ty):
            if self.player.has_key:
                self.game.event_bus.emit("level_completed")
            else:
                # дверь закрыта — нужен ключ
                self._show_message("Нужен ключ — найди его на уровне")
        self.camera.follow(self.player.tx, self.player.ty)

    def draw(self, surface):
        all_entities = list(self.items) + list(self.enemies) + [self.player]
        self.render_sys.draw(surface, self.level, all_entities, self.camera)
        self.render_sys.draw_enemy_hp(surface, self.enemies, self.camera)
        # факел поверх мира, но под HUD и debug
        self.render_sys.draw_lighting(surface, self.player, self.camera)
        fps = self.game.clock.get_fps()
        self.render_sys.draw_debug(surface, self.enemies, self.camera, fps)
        self.hud.draw(surface, self.player, self.level_num,
                      self.elapsed_time, self.message, self.message_timer)
        if self.paused:
            self._draw_pause(surface)

    def _draw_pause(self, surface):
        overlay = pygame.Surface((surface.get_width(), surface.get_height()))
        overlay.set_alpha(170)
        overlay.fill((0, 0, 0))
        surface.blit(overlay, (0, 0))
        font_big = self.game.resources.get_font(48)
        font = self.game.resources.get_font(22)
        cx = surface.get_width() // 2
        cy = surface.get_height() // 2
        title = font_big.render("Пауза", True, (255, 255, 255))
        surface.blit(title, title.get_rect(center=(cx, cy - 100)))
        lines = [
            "Esc — продолжить",
            "Q — в главное меню (сохранится)",
            "+ / - — громкость музыки",
            "",
            "В игре: Space — удар, F3 — отладка",
        ]
        for i, ln in enumerate(lines):
            s = font.render(ln, True, (220, 220, 220))
            surface.blit(s, s.get_rect(center=(cx, cy - 30 + i * 28)))


def _seed_for_level(level_num):
    base = 1000
    return base + level_num * 17
