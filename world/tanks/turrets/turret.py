

import math

import pygame
import pygame_util as util

from assets import assets
from camera import Camera
from constants import DEBUG_MODE
from world.bullet import Bullet

from ..rotation import move_pos_with_degrees


class Turret:
    DEFAULT_BULLET_SPEED = 4

    def __init__(self, pivot_pos: tuple[int, int], camera: Camera) -> None:
        self.camera = camera
        self.image = assets.images.tanks["blue_tank_barrel_1"]
        self.pivot_pos = pivot_pos
        self.bullet_speed = self.DEFAULT_BULLET_SPEED
        self.rotate(90)

    def set_pivot(self, pivot_pos: tuple[int, int]) -> None:
        self.pivot_pos = pivot_pos

    def update(self) -> None:
        self.rect = self.rotated_image.get_rect(center=self.pivot_pos)
        self.launch_pos = move_pos_with_degrees(self.pivot_pos, self.angle, 55)

    def rotate(self, angle: int) -> None:
        self.angle = angle
        self.rotated_image = pygame.transform.rotate(
            self.image, self.angle + 90)

    def fire(self, tank_id: int) -> Bullet:
        return Bullet(self.launch_pos, self.angle, self.bullet_speed, tank_id, self.camera)

    def render(self, screen: pygame.Surface) -> None:
        rect = self.rect.copy()
        rect.x, rect.y = self.camera.world_to_relative(self.rect.topleft)
        screen.blit(self.rotated_image, rect.topleft)

        if DEBUG_MODE:
            pos = self.camera.world_to_relative(self.pivot_pos)
            pygame.draw.circle(screen, util.Color.GREEN,
                               move_pos_with_degrees(pos, self.angle, 55), 4)
