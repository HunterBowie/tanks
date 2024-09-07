import pygame
import pygame_util as util

from assets import assets
from camera import Camera
from constants import DEBUG_MODE, BulletSize, ExplosionSize, TankColor

from .tanks.rotation import move_rect_with_degrees


class Bullet:
    RENDERING_LAYER = 4

    def __init__(self, pos: tuple[int, int], color: TankColor, size: BulletSize, explosion_size: ExplosionSize, seeking_force: float, angle: int, speed: int, tank_id: int, camera: Camera) -> None:
        self.camera = camera
        self.tank_id = tank_id
        self.speed = speed
        self.image = assets.images.bullets[f"{color.name.lower()}_bullet_{size.name.lower()}"]
        self.rect = self.image.get_rect(center=pos)
        self.rotate(angle)
        self.explosion_size = explosion_size
        self.explosion_timer = util.Timer()
        self.explosion_timer.start()
        self.seeking_force = seeking_force
        self.seeking_target_id: int = -1
        self.seeking_radius = 150
        self.seeking_timer = util.Timer()
        self.seeking_timer.start()

    def rotate(self, angle: int) -> None:
        self.angle = angle
        self.rotated_image = pygame.transform.rotate(
            self.image, self.angle - 90)

    def update(self) -> None:
        self.rect = self.rotated_image.get_rect(center=self.rect.center)
        move_rect_with_degrees(self.rect, self.angle, self.speed)

    def render(self, screen: pygame.Surface) -> None:
        rect = self.rect.copy()
        rect.topleft = self.camera.world_to_relative(rect.topleft)
        screen.blit(self.rotated_image, rect.topleft)
        if DEBUG_MODE:
            surf = pygame.Surface(
                (self.seeking_radius*2, self.seeking_radius*2), pygame.SRCALPHA)
            pygame.draw.circle(surf, util.Color.RED, (self.seeking_radius,
                               self.seeking_radius), self.seeking_radius)
            surf.set_alpha(50)
            screen.blit(surf, surf.get_rect(center=rect.center))
