
from typing import Protocol

import pygame

from camera import Camera


class WorldEntity(Protocol):
    def update(self) -> None:
        ...

    def render(self, screen: pygame.Surface) -> None:
        ...
