import math
from abc import ABC, abstractmethod

import pygame
import pygame_util as util

from assets import assets
from camera import Camera
from constants import DEBUG_MODE
from world.bullet import Bullet

from ..rotation import move_pos_with_degrees


class Turret(ABC):
    DEFAULT_BULLET_SPEED: int
    DEFAULT_FIRING_DELAY: int

    LAUNCH_POS_OFFSET: int = 67

    def __init__(self, pivot_pos: tuple[int, int], image: pygame.Surface, camera: Camera) -> None:
        self.camera = camera
        self.image = image
        self.pivot_pos = pivot_pos
        self.bullet_speed = self.DEFAULT_BULLET_SPEED
        self.firing_delay = self.DEFAULT_FIRING_DELAY
        self.firing_timer = util.Timer()
        self.firing_timer.start()
        self.rotate(90)

    def set_pivot(self, pivot_pos: tuple[int, int]) -> None:
        self.pivot_pos = pivot_pos

    def update(self) -> None:
        self.rect = self.rotated_image.get_rect(center=self.pivot_pos)
        self.launch_pos = move_pos_with_degrees(
            self.pivot_pos, self.angle, self.LAUNCH_POS_OFFSET)

    def rotate(self, angle: int) -> None:
        self.angle = angle
        self.rotated_image = pygame.transform.rotate(
            self.image, self.angle + 90)

    def firing_cooldown_reached(self) -> bool:
        if self.firing_timer.passed(self.firing_delay):
            return True
        return False

    @abstractmethod
    def _fire(self, tank_id: int) -> Bullet:
        pass

    def fire(self, tank_id: int) -> Bullet:
        self.firing_timer.start()
        return self._fire(tank_id)

    def render(self, screen: pygame.Surface) -> None:
        rect = self.rect.copy()
        rect.x, rect.y = self.camera.world_to_relative(self.rect.topleft)
        screen.blit(self.rotated_image, rect.topleft)

        if DEBUG_MODE:
            pos = self.camera.world_to_relative(self.pivot_pos)
            pygame.draw.circle(screen, util.Color.GREEN,
                               move_pos_with_degrees(pos, self.angle, self.LAUNCH_POS_OFFSET), 4)
            pygame.draw.circle(screen, util.Color.PURPLE, pos, 4)
