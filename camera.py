import pygame

from constants import MAX_ZOOM_FACTOR, MIN_ZOOM_FACTOR, SCREEN_SIZE


class Camera:
    """The position and zoom of the user on the terrain."""

    def __init__(self, center_pos: tuple[int, int]) -> None:
        screen_size = pygame.display.get_surface().get_size()
        self.x = center_pos[0] - screen_size[0]//2
        self.y = center_pos[1] - screen_size[1]//2
        self.zoom = 1.0

    @property
    def center(self) -> tuple[int, int]:
        screen_size = pygame.display.get_surface().get_size()
        center_x = self.x + screen_size[0]//2
        center_y = self.y + screen_size[1]//2
        return center_x, center_y

    def world_to_relative(self, world_pos: tuple[int, int]) -> tuple[int, int]:
        """Convert world coordinates to relative coordinates."""
        return round((world_pos[0] - self.x) * self.zoom), round((world_pos[1] - self.y) * self.zoom)

    def relative_to_world(self, relative_pos: tuple[int, int]) -> tuple[int, int]:
        """Convert relative coordinates to world coordinates."""
        return round(self.x + relative_pos[0] / self.zoom), round(self.y + relative_pos[1] / self.zoom)

    def move(self, x_change: int, y_change: int) -> None:
        """Move the camera so that the user sees a different part of the map."""
        self.x += x_change / self.zoom
        self.y += y_change / self.zoom

    def zoom_in(self) -> None:
        self._zoom(.2)

    def zoom_out(self) -> None:
        self._zoom(-.2)

    def _change_zoom_value(self, zoom_change: float) -> None:
        self.zoom += zoom_change
        self.zoom = round(self.zoom, 1)
        if self.zoom > MAX_ZOOM_FACTOR:
            self.zoom = MAX_ZOOM_FACTOR
        elif self.zoom < MIN_ZOOM_FACTOR:
            self.zoom = MIN_ZOOM_FACTOR

    def _zoom(self, zoom_change: float) -> None:
        screen_center = (SCREEN_SIZE[0] // 2, SCREEN_SIZE[1] // 2)
        world_center_before_zoom = self.relative_to_world(screen_center)

        self._change_zoom_value(zoom_change)
        while self.zoom in [0.6, 3.6, 3.2, 2.6, 2.2, 1.6, 1.2, 0.8, 1.8, 2.8]:
            self._change_zoom_value(zoom_change)

        world_center_after_zoom = self.relative_to_world(screen_center)

        self.x -= (world_center_after_zoom[0] -
                   world_center_before_zoom[0])
        self.y -= (world_center_after_zoom[1] -
                   world_center_before_zoom[1])
