class BaseScene:
    """Базовая сцена. Дети переопределяют handle_event, update, draw."""

    def __init__(self, game):
        self.game = game

    def handle_event(self, event):
        pass

    def update(self, dt):
        pass

    def draw(self, surface):
        pass
