
import pygame

from camera import Camera


class Effect:
    def update(self) -> None:
        pass

    def render(self, screen: pygame.Surface, camera: Camera) -> None:
        pass
