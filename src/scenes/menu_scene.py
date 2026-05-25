import os
import pygame

from src.scenes.base_scene import BaseScene
from src.core.constants import (
    SCREEN_WIDTH, SCREEN_HEIGHT,
    GAME, SAVE_FILE, STORY_FILE, HUD_COLOR,
)
from src.ui.menu import MenuButton, draw_buttons, draw_title


def load_story():
    if not os.path.exists(STORY_FILE):
        return ""
    try:
        with open(STORY_FILE, "r", encoding="utf-8") as f:
            return f.read().strip()
    except OSError:
        return ""


class MenuScene(BaseScene):
    def __init__(self, game):
        super().__init__(game)
        self.title_font = game.resources.get_font(54)
        self.btn_font = game.resources.get_font(28)
        self.small_font = game.resources.get_font(18)
        self.story = load_story()
        self.buttons = self.build_buttons()
        self.selected = 0
        game.resources.play_music("bg_loop.wav", volume=0.25)

    def build_buttons(self):
        btns = [MenuButton("Новая игра", "new")]
        if os.path.exists(SAVE_FILE):
            btns.append(MenuButton("Продолжить", "load"))
        btns.append(MenuButton("Выход", "quit"))
        return btns

    def handle_event(self, event):
        if event.type != pygame.KEYDOWN:
            return
        if event.key in (pygame.K_DOWN, pygame.K_s):
            self.selected = (self.selected + 1) % len(self.buttons)
        elif event.key in (pygame.K_UP, pygame.K_w):
            self.selected = (self.selected - 1) % len(self.buttons)
        elif event.key in (pygame.K_RETURN, pygame.K_SPACE):
            self.activate()

    def activate(self):
        action = self.buttons[self.selected].action
        if action == "new":
            self.game.change_scene(GAME, level_num=1, load_save=False)
        elif action == "load":
            self.game.change_scene(GAME, load_save=True)
        elif action == "quit":
            self.game.quit()

    def update(self, dt):
        pass

    def draw(self, surface):
        cx = SCREEN_WIDTH // 2
        draw_title(surface, self.title_font, "Носок-одиночка", cx, 120)
        if self.story:
            y = 200
            for line in self.story.split("\n"):
                if not line.strip():
                    y += 8
                    continue
                s = self.small_font.render(line, True, HUD_COLOR)
                rect = s.get_rect(center=(cx, y))
                surface.blit(s, rect)
                y += 22
        draw_buttons(surface, self.btn_font, self.buttons, self.selected,
                     cx, SCREEN_HEIGHT - 200)
        hint = self.small_font.render(
            "Стрелки/WASD — выбор, Enter — подтвердить",
            True, (160, 160, 170)
        )
        surface.blit(hint, hint.get_rect(center=(cx, SCREEN_HEIGHT - 30)))
