import pygame

from src.core.constants import (
    SCREEN_WIDTH, SCREEN_HEIGHT, FPS, WINDOW_TITLE, BG_COLOR,
    MENU, GAME, DEATH, WIN,
)
from src.core.input_manager import InputManager
from src.core.resource_manager import ResourceManager


class Game:
    """Главный объект. Держит цикл, активную сцену и общие менеджеры."""

    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption(WINDOW_TITLE)
        self.clock = pygame.time.Clock()
        self.input_manager = InputManager()
        self.resources = ResourceManager()
        self.running = True
        self.next_scene = None

        # стартуем с меню
        from src.scenes.menu_scene import MenuScene
        self.scene = MenuScene(self)

    def change_scene(self, scene_id, **kwargs):
        self.next_scene = (scene_id, kwargs)

    def apply_scene_change(self):
        if self.next_scene is None:
            return
        scene_id, kwargs = self.next_scene
        self.next_scene = None
        if scene_id == MENU:
            from src.scenes.menu_scene import MenuScene
            self.scene = MenuScene(self)
        elif scene_id == GAME:
            from src.scenes.game_scene import GameScene
            self.scene = GameScene(self, **kwargs)
        elif scene_id == DEATH:
            from src.scenes.death_scene import DeathScene
            self.scene = DeathScene(self)
        elif scene_id == WIN:
            from src.scenes.win_scene import WinScene
            self.scene = WinScene(self, **kwargs)

    def quit(self):
        self.running = False

    def run(self):
        while self.running:
            dt = self.clock.tick(FPS) / 1000.0
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                    continue
                self.scene.handle_event(event)
            self.input_manager.update(dt)
            self.scene.update(dt)
            self.screen.fill(BG_COLOR)
            self.scene.draw(self.screen)
            pygame.display.flip()
            self.apply_scene_change()
        pygame.quit()
