import os

import pygame
import pygame_util as util

CURRENT_DIR = os.path.dirname(__file__)

IMAGES_DIR = os.path.join(CURRENT_DIR, "images")
TILES_DIR = os.path.join(IMAGES_DIR, "tiles")
TURRETS_DIR = os.path.join(IMAGES_DIR, "turrets")
OBJECTS_DIR = os.path.join(IMAGES_DIR, "objects")
UI_DIR = os.path.join(IMAGES_DIR, "ui")
TANKS_DIR = os.path.join(IMAGES_DIR, "tanks")
BULLETS_DIR = os.path.join(IMAGES_DIR, "bullets")
EXPLOSIONS_DIR = os.path.join(IMAGES_DIR, "explosions")

SOUNDS_DIR = os.path.join(CURRENT_DIR, "sounds")
EFFECTS_DIR = os.path.join(SOUNDS_DIR, "effects")
MUSIC_DIR = os.path.join(SOUNDS_DIR, "music")

FONTS_DIR = os.path.join(CURRENT_DIR, "fonts")


class ImageManager:
    def __init__(self) -> None:
        self.tanks: dict[str, pygame.Surface] = {}
        self.turrets: dict[str, pygame.Surface] = {}
        self.bullets: dict[str, pygame.Surface] = {}
        self.explosions: dict[str, pygame.Surface] = {}
        self.tiles: dict[str, pygame.Surface] = {}
        self.objects: dict[str, pygame.Surface] = {}
        self.ui: dict[str, pygame.Surface] = {}
        self._other: dict[str, pygame.Surface] = {}

        self._load(TANKS_DIR, self.tanks)
        self._load(TURRETS_DIR, self.turrets)
        self._load(BULLETS_DIR, self.bullets)
        self._load(EXPLOSIONS_DIR, self.explosions)
        self._load(TILES_DIR, self.tiles)
        self._load(OBJECTS_DIR, self.objects)
        self._load(UI_DIR, self.ui)

        self._other['icon'] = pygame.transform.rotate(
            util.load_image('icon', IMAGES_DIR, convert=True), 270)

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


class SoundManager:
    def __init__(self) -> None:
        self.effects: dict[str, pygame.mixer.Sound] = {}
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


assets = AssetManager()
