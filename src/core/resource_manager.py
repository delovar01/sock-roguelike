import os
import pygame

from src.core.constants import ASSETS_DIR


class ResourceManager:
    """Кеш звуков и шрифтов."""

    def __init__(self):
        self.sounds = {}
        self.fonts = {}
        self.music_volume = 0.4
        try:
            pygame.mixer.init()
            self.sound_on = True
        except pygame.error:
            self.sound_on = False

    def play_sound(self, name, volume=0.6):
        if not self.sound_on:
            return
        if name not in self.sounds:
            path = os.path.join(ASSETS_DIR, "sounds", name)
            if not os.path.exists(path):
                return
            self.sounds[name] = pygame.mixer.Sound(path)
        s = self.sounds[name]
        s.set_volume(volume)
        s.play()

    def get_font(self, size):
        if size not in self.fonts:
            self.fonts[size] = pygame.font.SysFont("Arial", size)
        return self.fonts[size]

    def play_music(self, name, volume=None):
        if not self.sound_on:
            return
        path = os.path.join(ASSETS_DIR, "sounds", name)
        if not os.path.exists(path):
            return
        if volume is not None:
            self.music_volume = volume
        pygame.mixer.music.load(path)
        pygame.mixer.music.set_volume(self.music_volume)
        pygame.mixer.music.play(-1)

    def change_music_volume(self, delta):
        self.music_volume += delta
        if self.music_volume < 0:
            self.music_volume = 0
        if self.music_volume > 1:
            self.music_volume = 1
        if self.sound_on:
            pygame.mixer.music.set_volume(self.music_volume)
