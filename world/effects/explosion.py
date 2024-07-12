

import pygame
import pygame_util as util

from assets import assets
from camera import Camera
from world.tanks.tank import Tank


class Explosion:
    FRAME_DELAY = .1

    def __init__(self, pos: tuple[int, int], camera: Camera) -> None:
        self.camera = camera
        self.frames = [assets.images.explosions[name] for name in [
            "explosion1", "explosion2", "explosion3", "explosion4", "explosion5"]]
        self.frame = 0
        self.rect = self.frames[self.frame].get_rect(center=pos)
        self.frame_timer = util.Timer()
        self.frame_timer.start()
        self.dead = False

    def is_dead(self) -> bool:
        return self.dead

    def update(self):
        if self.frame_timer.passed(self.FRAME_DELAY):
            self.frame += 1
            if self.frame >= len(self.frames):
                self.dead = True
                self.frame_timer.start()
                self.frame_timer.reset()
            else:
                self.rect = self.frames[self.frame].get_rect(
                    center=self.rect.center)
            self.frame_timer.start()

    def render(self, screen: pygame.Surface) -> None:
        rect = self.rect.copy()
        rect.topleft = self.camera.world_to_relative(rect.topleft)
        screen.blit(self.frames[self.frame], rect)
