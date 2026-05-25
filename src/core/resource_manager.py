import pygame

from src.core.constants import ASSETS_DIR


class ResourceManager:
    """Кеш звуков и шрифтов. Чтобы каждый раз не грузить заново."""

    def __init__(self):
        self.sounds = {}
        self.fonts = {}
        self.music_volume = 0.4
        # на серверах без звука mixer может не подняться
        try:
            pygame.mixer.init()
            self.sound_enabled = True
        except pygame.error:
            self.sound_enabled = False

    def load_sound(self, name):
        if not self.sound_enabled:
            return None
        if name in self.sounds:
            return self.sounds[name]
        path = ASSETS_DIR / "sounds" / name
        if not path.exists():
            return None
        sound = pygame.mixer.Sound(str(path))
        self.sounds[name] = sound
        return sound

    def play_sound(self, name, volume=0.6):
        s = self.load_sound(name)
        if s is not None:
            s.set_volume(volume)
            s.play()

    def get_font(self, size):
        if size in self.fonts:
            return self.fonts[size]
        font = pygame.font.SysFont("Arial", size)
        self.fonts[size] = font
        return font

    def play_music(self, name, volume=None):
        if not self.sound_enabled:
            return
        path = ASSETS_DIR / "sounds" / name
        if not path.exists():
            return
        if volume is not None:
            self.music_volume = volume
        pygame.mixer.music.load(str(path))
        pygame.mixer.music.set_volume(self.music_volume)
        pygame.mixer.music.play(-1)  # -1 = бесконечный луп

    def change_music_volume(self, delta):
        self.music_volume += delta
        if self.music_volume < 0:
            self.music_volume = 0
        if self.music_volume > 1:
            self.music_volume = 1
        if self.sound_enabled:
            pygame.mixer.music.set_volume(self.music_volume)

    def stop_music(self):
        if self.sound_enabled:
            pygame.mixer.music.stop()
