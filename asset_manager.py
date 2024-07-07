import os

import pygame
import pygame_util as util

CURRENT_DIR = os.path.dirname(__file__)

IMAGES_DIR = os.path.join(CURRENT_DIR, "assets/images")
TILES_DIR = os.path.join(IMAGES_DIR, "tiles")
OBJECTS_DIR = os.path.join(IMAGES_DIR, "objects")
UI_DIR = os.path.join(IMAGES_DIR, "ui")
TANKS_DIR = os.path.join(IMAGES_DIR, "tanks")

SOUNDS_DIR = os.path.join(CURRENT_DIR, "assets/sounds")
EFFECTS_DIR = os.path.join(SOUNDS_DIR, "effects")
MUSIC_DIR = os.path.join(SOUNDS_DIR, "music")

FONTS_DIR = os.path.join(CURRENT_DIR, "assets/fonts")


class ImageManager:
    def __init__(self) -> None:
        self.tanks = {}
        self.tiles = {}
        self.objects = {}
        self.ui = {}
        self._other = {}

    def __getitem__(self, index: str) -> pygame.Surface:
        return self._other[index]

    @staticmethod
    def _load(directory: str, dictionary: dict) -> None:
        file_names = os.listdir(directory)
        file_names = [file_name.removesuffix(
            ".png") for file_name in file_names]
        file_names = [
            file_name for file_name in file_names if file_name[0] != "."]

        for name in file_names:
            dictionary[name] = util.load_image(name, directory, convert=True)

    def load(self) -> None:
        self._load(TILES_DIR, self.tiles)
        self._load(OBJECTS_DIR, self.objects)
        self._load(UI_DIR, self.ui)
        self._load(TANKS_DIR, self.tanks)

        self._other['icon'] = pygame.transform.rotate(
            util.load_image('icon', IMAGES_DIR, convert=True), 270)


class SoundManager:
    def __init__(self) -> None:
        self.effects = {}
        self.music = {}
        self._load(EFFECTS_DIR, self.effects)
        self._load(MUSIC_DIR, self.music)

    @staticmethod
    def _load(directory: str, dictionary: dict) -> None:
        file_names = os.listdir(directory)

        for file_name in file_names:
            dictionary[file_name[:-4]
                       ] = pygame.mixer.Sound(os.path.join(directory, file_name))


class AssetManager:
    def __init__(self) -> None:
        self.images = ImageManager()
        self.sounds = SoundManager()
        self.fonts = {"kenney_wide": os.path.join(
            FONTS_DIR, "kenney_wide.ttf")}

    def load_images(self) -> None:
        """You may only call this method once the pygame display has been initalized."""
        self.images.load()
