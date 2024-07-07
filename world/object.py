from __future__ import annotations

from dataclasses import dataclass

import pygame

from asset_manager import AssetManager


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
