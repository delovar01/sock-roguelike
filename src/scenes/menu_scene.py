import pygame

from src.scenes.base_scene import BaseScene
from src.core.constants import (
    SCREEN_WIDTH, SCREEN_HEIGHT, SceneId, SAVE_FILE, STORY_FILE, HUD_COLOR
)
from src.ui.menu import MenuButton, draw_buttons, draw_title


def _load_story():
    if STORY_FILE.exists():
        try:
            return STORY_FILE.read_text(encoding="utf-8").strip()
        except OSError:
            return ""
    return ""


class MenuScene(BaseScene):
    def __init__(self, game):
        super().__init__(game)
        self.title_font = game.resources.get_font(54)
        self.btn_font = game.resources.get_font(28)
        self.small_font = game.resources.get_font(18)
        self._story = _load_story()
        self._buttons = self._build_buttons()
        self._selected = 0
        game.resources.play_music("bg_loop.wav", volume=0.25)

    def _build_buttons(self):
        btns = [MenuButton("Новая игра", "new")]
        if SAVE_FILE.exists():
            btns.append(MenuButton("Продолжить", "load"))
        btns.append(MenuButton("Выход", "quit"))
        return btns

    def handle_event(self, event):
        if event.type != pygame.KEYDOWN:
            return
        if event.key in (pygame.K_DOWN, pygame.K_s):
            self._selected = (self._selected + 1) % len(self._buttons)
        elif event.key in (pygame.K_UP, pygame.K_w):
            self._selected = (self._selected - 1) % len(self._buttons)
        elif event.key in (pygame.K_RETURN, pygame.K_SPACE):
            self._activate()

    def _activate(self):
        action = self._buttons[self._selected].action
        if action == "new":
            self.game.change_scene(SceneId.GAME, level_num=1, load_save=False)
        elif action == "load":
            self.game.change_scene(SceneId.GAME, load_save=True)
        elif action == "quit":
            self.game.quit()

    def update(self, dt):
        pass

    def draw(self, surface):
        cx = SCREEN_WIDTH // 2
        draw_title(surface, self.title_font, "Носок-одиночка", cx, 120)
        if self._story:
            # рисуем по строкам
            y = 200
            for line in self._story.split("\n"):
                if not line.strip():
                    y += 8
                    continue
                s = self.small_font.render(line, True, HUD_COLOR)
                rect = s.get_rect(center=(cx, y))
                surface.blit(s, rect)
                y += 22
        draw_buttons(surface, self.btn_font, self._buttons, self._selected,
                     cx, SCREEN_HEIGHT - 200)
        hint = self.small_font.render(
            "Стрелки/WASD — выбор, Enter — подтвердить",
            True, (160, 160, 170)
        )
        surface.blit(hint, hint.get_rect(center=(cx, SCREEN_HEIGHT - 30)))
