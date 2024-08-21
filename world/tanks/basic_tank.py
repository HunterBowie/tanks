
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

from .rotation import move_rect_with_degrees


class BasicTank(Tank):
    DEFAULT_SPEED = 3
    MAX_HEALTH = 100

    def __init__(self, pos: tuple[int, int], color: TankColor, camera: Camera) -> None:
        self.turret = BasicTurret(pos, color, camera)
        self.color = color
        super().__init__(pos, assets.images.tanks[f"{color.name.lower()}_tank_body"], [
            self.turret], TankTrackSize.SMALL, camera)

    def update(self) -> None:
        x, y = self.rect.center
        angle = 180-self.turret.angle
        radians = math.radians(angle)
        x += 6 * math.cos(radians)
        y += 6 * math.sin(radians)
        self.turret.set_pivot((x, y))
        super().update()
