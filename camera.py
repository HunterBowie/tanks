import pygame

from constants import SCREEN_SIZE


class Camera:
    FOLLOW_DELAY_X = 0.02
    FOLLOW_DELAY_Y = 0.02
    MAX_ZOOM_FACTOR = 3
    MIN_ZOOM_FACTOR = .2
    """The position and zoom of the user on the terrain."""

    def __init__(self) -> None:
        self.rect = pygame.display.get_surface().get_rect()
        self.barrier_rects = []
        self.zoom = 1.0

    def set_pos(self, pos: tuple[int, int]) -> None:
        self.rect.center = pos

    def set_barrier_rects(self, barrier_rects: list[pygame.Rect]) -> None:
        self.barrier_rects = barrier_rects

    def world_to_relative(self, world_pos: tuple[int, int]) -> tuple[int, int]:
        """Convert world coordinates to relative coordinates."""
        return round((world_pos[0] - self.rect.x) * self.zoom), round((world_pos[1] - self.rect.y) * self.zoom)

    def relative_to_world(self, relative_pos: tuple[int, int]) -> tuple[int, int]:
        """Convert relative coordinates to world coordinates."""
        return round(self.rect.x + relative_pos[0] / self.zoom), round(self.rect.y + relative_pos[1] / self.zoom)

    def move(self, x_change: int, y_change: int) -> None:
        "Move the camera relative to zoom."
        self.rect.x += x_change / self.zoom
        self.rect.y += y_change / self.zoom

    def move_within_barriers(self, x_change: int, y_change: int) -> None:
        """Move the camera so that it stays within the world barriers."""
        if x_change != 0:
            self.move(x_change, 0)
            for rect in self.barrier_rects:
                if rect.colliderect(self.rect):
                    self.move(-x_change, 0)
                    break

        if y_change != 0:
            self.move(0, y_change)
            for rect in self.barrier_rects:
                if rect.colliderect(self.rect):
                    self.move(0, -y_change)
                    break

    def move_with_delay_within_barriers(self, target: tuple[int, int]) -> None:
        "Move the camera towards a target within the world borders."
        camera_dx = (target[0] - self.rect.centerx)
        camera_dy = (target[1] - self.rect.centery)
        camera_dx *= self.FOLLOW_DELAY_X
        camera_dy *= self.FOLLOW_DELAY_Y
        self.move_within_barriers(round(camera_dx), round(camera_dy))

    def zoom_in(self) -> None:
        self._zoom(.2)

    def zoom_out(self) -> None:
        self._zoom(-.2)

    def _change_zoom_value(self, zoom_change: float) -> None:
        self.zoom += zoom_change
        self.zoom = round(self.zoom, 1)
        if self.zoom > self.MAX_ZOOM_FACTOR:
            self.zoom = self.MAX_ZOOM_FACTOR
        elif self.zoom < self.MIN_ZOOM_FACTOR:
            self.zoom = self.MIN_ZOOM_FACTOR

    def _zoom(self, zoom_change: float) -> None:
        screen_center = (SCREEN_SIZE[0] // 2, SCREEN_SIZE[1] // 2)
        world_center_before_zoom = self.relative_to_world(screen_center)

        self._change_zoom_value(zoom_change)
        while self.zoom in [0.6, 3.6, 3.2, 2.6, 2.2, 1.6, 1.2, 0.8, 1.8, 2.8]:
            self._change_zoom_value(zoom_change)

        world_center_after_zoom = self.relative_to_world(screen_center)

        self.rect.x -= (world_center_after_zoom[0] -
                        world_center_before_zoom[0])
        self.rect.y -= (world_center_after_zoom[1] -
                        world_center_before_zoom[1])
