
import pygame
import pygame_util as util

from assets import assets
from camera import Camera
from constants import TankTrackSize
from world.tanks.tank import Tank


class TrackEffect:
    ALIVE_TIME_SECONDS = 20
    RENDERING_LAYER = 1

    def __init__(self, tank: Tank, camera: Camera) -> None:
        self.camera = camera
        self.image = assets.images.objects[tank.track_size.value]
        if tank.track_size == TankTrackSize.SMALL:
            self.image = pygame.transform.scale(self.image, (70, 70))
        self.image = pygame.transform.rotate(self.image, tank.angle + 90)
        self.rect = self.image.get_rect()
        self.rect.center = tank.rect.center
        self.alive_timer = util.Timer()
        self.alive_timer.start()

    def is_finished(self) -> bool:
        return self.alive_timer.passed(self.ALIVE_TIME_SECONDS)

    def update(self):
        self.image.set_alpha(255 - util.map_values(
            self.alive_timer.get(), 0, self.ALIVE_TIME_SECONDS, 0, 255))

    def render(self, screen: pygame.Surface) -> None:
        rel_pos = self.camera.world_to_relative(self.rect.topleft)
        screen.blit(self.image, rel_pos)
