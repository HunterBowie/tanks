
from typing import Protocol

import pygame

from camera import Camera


class Entity(Protocol):
    RENDERING_LAYER: int
    rect: pygame.Rect

    def update(self) -> None:
        ...

    def render(self, screen: pygame.Surface) -> None:
        ...
