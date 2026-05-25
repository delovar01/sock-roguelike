class EventBus:
    """Простая шина событий. Кто-то подписывается, кто-то вызывает emit."""

    def __init__(self):
        self.subs = {}

    def subscribe(self, name, callback):
        if name not in self.subs:
            self.subs[name] = []
        self.subs[name].append(callback)

    def emit(self, name):
        for cb in self.subs.get(name, []):
            cb()

    def clear(self):
        self.subs.clear()
