
from __future__ import annotations

import math

import pygame
import pygame_util as util

from assets import assets
from camera import Camera
from constants import TankTrackSize
from world.tanks.tank import Tank
from world.tanks.turrets.seeking_turret import SeekingTurret


class SeekingTank(Tank):
    DEFAULT_SPEED = 2
    MAX_HEALTH = 100

    LEFT_TURRET_OFFSET = -20, 15
    RIGHT_TURRET_OFFSET = 20, 15

    def __init__(self, pos: tuple[int, int], camera: Camera) -> None:
        super().__init__(
            pos, assets.images.tanks[f"special_tank_body_1"], TankTrackSize.LARGE, camera)
        self.attach_turret(SeekingTurret(
            (pos[0]+self.LEFT_TURRET_OFFSET[0], pos[1]+self.LEFT_TURRET_OFFSET[1]), camera))
        self.attach_turret(SeekingTurret(
            (pos[0]+self.RIGHT_TURRET_OFFSET[0], pos[1]+self.RIGHT_TURRET_OFFSET[1]), camera))
