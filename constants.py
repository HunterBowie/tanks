SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 600
SCREEN_SIZE = SCREEN_WIDTH, SCREEN_HEIGHT


TILE_SIZE = 64
TERRAIN_DIRECTORY = "terrain"

MAX_ZOOM_FACTOR = 3
MIN_ZOOM_FACTOR = .2


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
