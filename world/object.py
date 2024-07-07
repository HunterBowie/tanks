from __future__ import annotations

from dataclasses import dataclass

import pygame

from asset_manager import AssetManager
from camera import Camera


@dataclass
class Object:
    x: int
    y: int
    name: str
    image: pygame.Surface

    @staticmethod
    def load(data: dict, assets: AssetManager) -> Object:
        return Object(data["x"], data["y"], data["name"], assets.images.tiles[data["name"]])

    def unload(self) -> dict:
        return {"x": self.x, "y": self.y, "name": self.name}

    def update(self) -> None:
        pass

    def render(self, screen: pygame.Surface, camera: Camera) -> None:
        pos = camera.world_to_relative((self.x, self.y))
        screen.blit(pygame.transform.scale(self.image, (int(self.image.get_width(
        ) * camera.zoom), int(self.image.get_height() * camera.zoom))), pos)
