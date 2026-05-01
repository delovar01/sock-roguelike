from abc import ABC, abstractmethod


class BaseScene(ABC):
    """Базовая сцена. Каждая сцена имеет 3 метода — узкий интерфейс."""

    def __init__(self, game):
        self.game = game

    @abstractmethod
    def handle_event(self, event):
        ...

    @abstractmethod
    def update(self, dt):
        ...

    @abstractmethod
    def draw(self, surface):
        ...
