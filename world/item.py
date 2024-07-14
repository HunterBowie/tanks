
from __future__ import annotations

import pygame

from camera import Camera


class Item:
    RENDERING_LAYER = 2

    @staticmethod
    def load(data: dict) -> Item:
        pass

    def unload(self) -> dict:
        pass

    def update(self) -> None:
        pass

    def render(self, screen: pygame.Surface) -> None:
        pass
