import pygame

from src.core.constants import (
    SCREEN_WIDTH, SCREEN_HEIGHT, FPS, WINDOW_TITLE, BG_COLOR, SceneId
)
from src.core.event_bus import EventBus
from src.core.input_manager import InputManager
from src.core.resource_manager import ResourceManager


class Game:
    """Главный объект. Держит цикл, активную сцену и общие менеджеры."""

    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption(WINDOW_TITLE)
        self.clock = pygame.time.Clock()

        self.event_bus = EventBus()
        self.input_manager = InputManager()
        self.resources = ResourceManager()

        self._running = True
        self._scene = None
        self._next_scene = None

        # импортируем тут, чтобы избежать кольцевых импортов
        from src.scenes.menu_scene import MenuScene
        self._scene = MenuScene(self)

    def change_scene(self, scene_id, **kwargs):
        # сцены создаём отложенно — после текущего апдейта
        self._next_scene = (scene_id, kwargs)

    def _apply_scene_change(self):
        if self._next_scene is None:
            return
        scene_id, kwargs = self._next_scene
        self._next_scene = None
        self.event_bus.clear()
        if scene_id == SceneId.MENU:
            from src.scenes.menu_scene import MenuScene
            self._scene = MenuScene(self)
        elif scene_id == SceneId.GAME:
            from src.scenes.game_scene import GameScene
            self._scene = GameScene(self, **kwargs)
        elif scene_id == SceneId.DEATH:
            from src.scenes.death_scene import DeathScene
            self._scene = DeathScene(self)
        elif scene_id == SceneId.WIN:
            from src.scenes.win_scene import WinScene
            self._scene = WinScene(self)

    def quit(self):
        self._running = False

    def run(self):
        while self._running:
            dt = self.clock.tick(FPS) / 1000.0
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self._running = False
                    continue
                # одноразовые действия (Esc, пробел, F3, меню) — через handle_event
                self._scene.handle_event(event)

            # клавиши движения с авто-повтором — отдельно, каждый кадр
            self.input_manager.update(dt)

            self._scene.update(dt)
            self.screen.fill(BG_COLOR)
            self._scene.draw(self.screen)
            pygame.display.flip()

            self._apply_scene_change()

        pygame.quit()
