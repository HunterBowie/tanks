
import pygame

from camera import Camera


class Item:

    def unload(self) -> dict:
        pass

    def update(self) -> None:
        pass

    def render(self, screen: pygame.Surface) -> None:
        pass
