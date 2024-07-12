
from __future__ import annotations

import math

import pygame
import pygame_util as util

from assets import assets
from camera import Camera
from constants import TankTrackSize
from world.tanks.bullet import Bullet
from world.tanks.turret import Turret

from .rotation import get_angle, move_rect_with_degrees


class Tank:
    ID = 0

    def __init__(self, pos: tuple[int, int], camera: Camera) -> None:
        self.camera = camera
        self.image = assets.images.tanks["blue_tank_body"]
        self.rect = self.image.get_rect(center=pos)
        self.rotated_image = self.image
        self.rotate(90)
        self.speed = 3
        self.track_size = TankTrackSize.SMALL
        self.track_timer = util.Timer()
        self.track_timer.start()
        self.id = self.generate_id()

        self.turret = Turret(self.rect.center, self.id, camera)

    @property
    def mask(self) -> pygame.Mask:
        return pygame.mask.from_surface(self.rotated_image)

    @classmethod
    def generate_id(cls) -> int:
        cls.ID += 1
        return cls.ID

    def move(self, angle: int, other_tanks: list[Tank]) -> None:
        original_angle = self.angle
        self.rotate(angle)
        for tank in other_tanks:
            if tank.mask.overlap(self.mask, (self.rect.x - tank.rect.x, self.rect.y - tank.rect.y)):
                self.rotate(original_angle)
                break
        move_rect_with_degrees(self.rect, angle, self.speed)
        for tank in other_tanks:
            if tank.mask.overlap(self.mask, (self.rect.x - tank.rect.x, self.rect.y - tank.rect.y)):
                move_rect_with_degrees(self.rect, angle-180, self.speed)
                break

    def rotate(self, angle: int) -> None:
        self.rotated_image = pygame.transform.rotate(self.image, angle + 90)
        self.angle = angle
        self.rect = self.rotated_image.get_rect(center=self.rect.center)

    def fire(self) -> list[Bullet]:
        return [self.turret.fire()]

    def update(self) -> None:
        x, y = self.rect.center
        angle = 180-self.turret.angle
        radians = math.radians(angle)
        x += 6 * math.cos(radians)
        y += 6 * math.sin(radians)
        self.turret.set_pivot((x, y))
        self.turret.update()

    def render(self, screen: pygame.Surface) -> None:
        rect = self.rect.copy()
        rect.topleft = self.camera.world_to_relative(rect.topleft)
        # screen.blit(self.mask.to_surface(), rect.topleft)
        screen.blit(self.rotated_image, rect)
        self.turret.render(screen)
