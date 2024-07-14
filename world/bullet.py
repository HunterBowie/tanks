import pygame
import pygame_util as util

from assets import assets
from camera import Camera

from .tanks.rotation import move_rect_with_degrees


class Bullet:
    RENDERING_LAYER = 4

    def __init__(self, pos: tuple[int, int], angle: int, speed: int, tank_id: int, camera: Camera) -> None:
        self.camera = camera
        self.tank_id = tank_id
        self.speed = speed
        self.image = assets.images.bullets["blue_bullet_1"]
        self.rect = self.image.get_rect(center=pos)
        self.rotate(angle)
        self.explosion_timer = util.Timer()
        self.explosion_timer.start()

    def rotate(self, angle: int) -> None:
        self.angle = angle
        self.rotated_image = pygame.transform.rotate(
            self.image, self.angle - 90)

    def update(self) -> None:
        self.rect = self.rotated_image.get_rect(center=self.rect.center)
        move_rect_with_degrees(self.rect, self.angle, self.speed)

    def render(self, screen: pygame.Surface) -> None:
        rect = self.rect.copy()
        rect.topleft = self.camera.world_to_relative(rect.topleft)
        screen.blit(self.rotated_image, rect.topleft)
