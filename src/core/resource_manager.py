import pygame

from src.core.constants import ASSETS_DIR


class ResourceManager:
    """Кеш звуков и шрифтов. Грузим один раз — используем много."""

    def __init__(self):
        self._sounds = {}
        self._fonts = {}
        self._sound_enabled = True
        try:
            pygame.mixer.init()
        except pygame.error:
            self._sound_enabled = False

    def load_sound(self, name):
        if not self._sound_enabled:
            return None
        if name in self._sounds:
            return self._sounds[name]
        path = ASSETS_DIR / "sounds" / name
        if not path.exists():
            return None
        try:
            sound = pygame.mixer.Sound(str(path))
            self._sounds[name] = sound
            return sound
        except pygame.error:
            return None

    def play_sound(self, name, volume=0.6):
        s = self.load_sound(name)
        if s is not None:
            s.set_volume(volume)
            s.play()

    def get_font(self, size):
        if size in self._fonts:
            return self._fonts[size]
        font = pygame.font.SysFont("Arial", size)
        self._fonts[size] = font
        return font

    def play_music(self, name, volume=0.4):
        if not self._sound_enabled:
            return
        path = ASSETS_DIR / "sounds" / name
        if not path.exists():
            return
        try:
            pygame.mixer.music.load(str(path))
            pygame.mixer.music.set_volume(volume)
            pygame.mixer.music.play(-1)
        except pygame.error:
            pass

    def stop_music(self):
        try:
            pygame.mixer.music.stop()
        except pygame.error:
            pass
