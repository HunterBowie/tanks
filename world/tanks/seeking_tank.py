
from __future__ import annotations

import math

import pygame
import pygame_util as util

from assets import assets
from camera import Camera
from constants import DEBUG_MODE, TankColor, TankTrackSize
from world.bullet import Bullet
from world.tanks.tank import Tank
from world.tanks.turrets import BasicTurret
from world.tanks.turrets.seeking_turret import SeekingTurret
from world.tanks.turrets.turret import Turret

from .rotation import move_rect_with_degrees


def move_point_around_origin(point: tuple[int, int], angle: int) -> tuple[int, int]:
    point = point[0], -point[1]

    x = point[0]*math.cos(math.radians(angle)) - \
        point[1]*math.sin(math.radians(angle))
    y = point[0]*math.sin(math.radians(angle)) + \
        point[1]*math.cos(math.radians(angle))

    return x, -y


class SeekingTank(Tank):
    DEFAULT_SPEED = 2
    MAX_HEALTH = 100

    def __init__(self, pos: tuple[int, int], camera: Camera) -> None:
        self.left_turret_offset = -20, 15
        self.right_turret_offset = 20, 15
        self.left_turret = SeekingTurret(
            (pos[0]+self.left_turret_offset[0], pos[1]+self.left_turret_offset[1]), camera)
        self.right_turret = SeekingTurret(
            (pos[0]+self.right_turret_offset[0], pos[1]+self.right_turret_offset[1]), camera)
        super().__init__(pos, assets.images.tanks[f"special_tank_body_1"],
                         [self.left_turret, self.right_turret], TankTrackSize.SMALL, camera)

    def _pos_turret(self, turret: Turret, offset: tuple[int, int]) -> None:
        angle_offset = self.angle - 90
        if angle_offset == 0:
            new_offset = offset
        else:
            new_offset = move_point_around_origin(offset, angle_offset)
        turret.set_pivot(
            (self.rect.centerx+new_offset[0], self.rect.centery+new_offset[1]))

    def update(self) -> None:
        self._pos_turret(self.left_turret, (self.left_turret_offset))
        self._pos_turret(self.right_turret, (self.right_turret_offset))
        super().update()
