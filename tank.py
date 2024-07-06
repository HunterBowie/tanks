

import pygame

from camera import Camera


class Tank:
    def __init__(self, world_x: int, world_y: int, image: pygame.Surface) -> None:
        self.world_x = world_x
        self.world_y = world_y
        self.image = image

    def render(self, screen: pygame.Surface, camera: Camera) -> None:
        rel_pos = camera.world_to_relative((self.world_x, self.world_y))
        screen.blit(self.image, rel_pos)
