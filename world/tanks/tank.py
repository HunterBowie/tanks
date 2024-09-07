
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

from .rotation import move_rect_with_degrees, rotate_point_around_origin


class Tank(ABC):
    DEFAULT_SPEED: int
    MAX_HEALTH: int
    RENDERING_LAYER = 3
    _ID = 0

    def __init__(self, pos: tuple[int, int], image: pygame.Surface, track_size: TankTrackSize, camera: Camera) -> None:
        self.camera = camera
        self.turrets = []
        self.turret_offsets = []

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

    def attach_turret(self, turret: Turret) -> None:
        try:
            offset = turret.pivot_pos[0] - \
                self.rect.centerx, turret.pivot_pos[1]-self.rect.centery
        except AttributeError:
            raise Exception(
                "You must initialize the tank (ie. super.__init__) before calling attach turret)")
        self.turrets.append(turret)
        self.turret_offsets.append(offset)

    def _pos_turret(self, turret: Turret, offset: tuple[int, int]) -> None:
        angle_offset = self.angle - 90
        if angle_offset == 0:
            new_offset = offset
        else:
            new_offset = rotate_point_around_origin(offset, angle_offset)
        turret.set_pivot(
            (self.rect.centerx+new_offset[0], self.rect.centery+new_offset[1]))

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

    def firing_cooldown_reached(self) -> bool:
        for turret in self.turrets:
            if turret.firing_cooldown_reached():
                return True
        return False

    def fire(self) -> list[Bullet]:
        return [turret.fire(self.id) for turret in self.turrets if turret.firing_cooldown_reached()]

    def update(self) -> None:
        for turret in self.turrets:
            self._pos_turret(
                turret, self.turret_offsets[self.turrets.index(turret)])
            turret.update()

    def render_health_bar(self, screen: pygame.Surface) -> None:
        rect = self.rect.copy()
        rect.topleft = self.camera.world_to_relative(rect.topleft)
        health_rect = pygame.Rect(0, rect.y-30, 100, 20)
        health_rect.centerx = rect.centerx

        pygame.draw.rect(screen, util.Color.GREEN, health_rect)

    def render(self, screen: pygame.Surface) -> None:
        rect = self.rect.copy()
        rect.topleft = self.camera.world_to_relative(rect.topleft)
        if DEBUG_MODE:
            screen.blit(self.mask.to_surface(), rect.topleft)
            util.Text(str(self.id), rect.x, rect.y-30).render(screen)
        else:
            screen.blit(self.rotated_image, rect)

        for turret in self.turrets:
            turret.render(screen)
