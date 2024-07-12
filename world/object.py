from __future__ import annotations

from dataclasses import dataclass

import pygame

from assets import assets
from camera import Camera


@dataclass
class Object:
    x: int
    y: int
    name: str
    image: pygame.Surface
    camera: Camera

    @staticmethod
    def load(data: dict, camera: Camera) -> Object:
        return Object(data["x"], data["y"], data["name"], assets.images.tiles[data["name"]], Camera)

    def unload(self) -> dict:
        return {"x": self.x, "y": self.y, "name": self.name}

    def update(self) -> None:
        pass

    def render(self, screen: pygame.Surface) -> None:
        pos = self.camera.world_to_relative((self.x, self.y))
        screen.blit(pygame.transform.scale(self.image, (int(self.image.get_width(
        ) * self.camera.zoom), int(self.image.get_height() * self.camera.zoom))), pos)
