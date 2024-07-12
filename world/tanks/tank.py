
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

        self.turret = Turret(self.rect.center, camera)

    def move(self, angle: int) -> None:
        self.rotate(angle)
        move_rect_with_degrees(self.rect, angle, self.speed)

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
        rel_pos = self.camera.world_to_relative((self.rect.x, self.rect.y))
        screen.blit(self.rotated_image, rel_pos)
        self.turret.render(screen)
