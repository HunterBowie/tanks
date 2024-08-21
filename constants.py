from enum import Enum, StrEnum, auto
from os import path

SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 600
SCREEN_SIZE = SCREEN_WIDTH, SCREEN_HEIGHT


TILE_SIZE = 64
CURRENT_DIR = path.dirname(__file__)
WORLDS_DIR = path.join(CURRENT_DIR, "worlds")

NUM_RENDERING_LAYERS = 5

DEBUG_MODE = False


class TankTrackSize(StrEnum):
    SMALL = "tracksSmall"
    LARGE = "tracksLarge"
    DOUBLE = "tracksDouble"


class TankColor(Enum):
    RED = auto()
    BLUE = auto()
    GREEN = auto()
    BEIGE = auto()
    BLACK = auto()


class BulletSize(Enum):
    BASIC = auto()
    WIDE = auto()
    NARROW = auto()


class MouseButton:
    class Pressed:
        LEFT = 0
        RIGHT = 2

    class Down:
        MIDDLE = 2
        SCROLL_UP = 4
        SCROLL_DOWN = 5
        SIDE_BACK = 6
        SIDE_FRONT = 7


class EntityType(Enum):
    EFFECT = auto()
    TILE = auto()
    ITEM = auto()
    OBJECT = auto()
    TANK = auto()
    BULLET = auto()
