"""Простая шина событий — паттерн Observer.

Системы могут эмитить события и подписываться на них,
не зная друг о друге напрямую.
"""


class EventBus:
    def __init__(self):
        self._subs = {}

    def subscribe(self, event_name, callback):
        if event_name not in self._subs:
            self._subs[event_name] = []
        self._subs[event_name].append(callback)

    def emit(self, event_name, **payload):
        for cb in self._subs.get(event_name, []):
            cb(**payload)

    def clear(self):
        self._subs.clear()
