
from __future__ import annotations

import math
from abc import ABC, abstractmethod

import pygame
import pygame_util as util

from assets import assets
from camera import Camera
from constants import DEBUG_MODE, TankTrackSize
from world.bullet import Bullet
from world.tanks.turrets.turret import Turret

from .rotation import move_rect_with_degrees


class Tank(ABC):
    DEFAULT_SPEED: int
    MAX_HEALTH: int
    RENDERING_LAYER = 3
    _ID = 0

    def __init__(self, pos: tuple[int, int], image: pygame.Surface,
                 turrets: list[Turret], track_size: TankTrackSize, camera: Camera) -> None:
        self.camera = camera
        self.turrets = turrets

        self.image = image
        self.rotated_image = self.image.copy()
        self.rect = self.image.get_rect(center=pos)
        self.rotate(90)

        self.track_size = track_size
        self.track_timer = util.Timer()
        self.track_timer.start()

        self.speed = self.DEFAULT_SPEED
        self.health = self.MAX_HEALTH
        self.id = self._generate_id()

    @staticmethod
    def _generate_id() -> int:
        Tank._ID += 1
        return Tank._ID

    @property
    def mask(self) -> pygame.Mask:
        return pygame.mask.from_surface(self.rotated_image)

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
        return [turret.fire(self.id) for turret in self.turrets if turret.firing_cooldown_reached()]

    @abstractmethod
    def update(self) -> None:
        for turret in self.turrets:
            turret.update()

    def render(self, screen: pygame.Surface) -> None:
        rect = self.rect.copy()
        rect.topleft = self.camera.world_to_relative(rect.topleft)
        if DEBUG_MODE:
            screen.blit(self.mask.to_surface(), rect.topleft)
        else:
            screen.blit(self.rotated_image, rect)

        for turret in self.turrets:
            turret.render(screen)
