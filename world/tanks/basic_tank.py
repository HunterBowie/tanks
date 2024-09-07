
from __future__ import annotations

import math

import pygame
import pygame_util as util

from assets import assets
from camera import Camera
from constants import DEBUG_MODE, TankColor, TankTrackSize, TurretType
from world.bullet import Bullet
from world.tanks.tank import Tank
from world.tanks.turrets import BasicTurret
from world.tanks.turrets.barrel_turret import BarrelTurret
from world.tanks.turrets.wide_turret import WideTurret

from .rotation import move_rect_with_degrees


class BasicTank(Tank):
    DEFAULT_SPEED = 3
    MAX_HEALTH = 100

    TURRET_OFFSET = 0, -5

    def __init__(self, pos: tuple[int, int], turret_type: TurretType, color: TankColor, camera: Camera) -> None:
        super().__init__(pos,
                         assets.images.tanks[f"{color.name.lower()}_tank_body"], TankTrackSize.SMALL, camera)
        self.color = color
        self.turret_type = turret_type
        turret_x, turret_y = pos[0] + \
            self.TURRET_OFFSET[0], pos[1]+self.TURRET_OFFSET[1]
        if turret_type == TurretType.BASIC:
            self.attach_turret(BasicTurret(
                (turret_x, turret_y), color, camera))
        elif turret_type == TurretType.BARREL:
            self.attach_turret(BarrelTurret(
                (turret_x, turret_y), color, camera))
        elif turret_type == TurretType.WIDE:
            self.attach_turret(WideTurret(
                (turret_x, turret_y), color, camera))
