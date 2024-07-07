
import math

import pygame

from camera import Camera


class Tank:
    def __init__(self, pos: tuple[int, int], image: pygame.Surface) -> None:
        self.rect = pygame.Rect(
            pos[0], pos[1], image.get_width(), image.get_height())
        self.image = image
        self.rotated_image = self.image
        self.rotate(90)
        self.speed = 3

    def move(self, angle: int) -> None:
        self.rotate(angle)
        self.move_with_degrees(angle)

    def move_with_degrees(self, angle: int) -> None:
        radians = math.radians(angle)
        self.rect.x += self.speed * math.cos(radians)
        self.rect.y -= self.speed * math.sin(radians)

    def rotate(self, angle: int) -> None:
        self.rotated_image = pygame.transform.rotate(self.image, angle + 90)
        self.angle = angle
        self.rect = self.rotated_image.get_rect(center=self.rect.center)

    def update(self) -> None:
        pass

    def render(self, screen: pygame.Surface, camera: Camera) -> None:
        rel_pos = camera.world_to_relative((self.rect.x, self.rect.y))
        screen.blit(self.rotated_image, rel_pos)
