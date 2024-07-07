from __future__ import annotations

from dataclasses import dataclass

import pygame

from asset_manager import AssetManager
from camera import Camera
from constants import TILE_SIZE


@dataclass
class Tile:
    row: int
    col: int
    name: str
    image: pygame.Surface

    def get_rel_rect(self, camera: Camera) -> pygame.Rect:
        rel_tile_size = TILE_SIZE * camera.zoom
        row, col = self.row, self.col
        world_pos = col * rel_tile_size, row * rel_tile_size
        rel_x, rel_y = camera.world_to_relative(world_pos)
        return pygame.Rect(rel_x, rel_y, rel_tile_size, rel_tile_size)

    @staticmethod
    def load(data: dict, assets: AssetManager) -> Tile:
        return Tile(data["row"], data["col"], data["name"], assets.images.tiles[data["name"]])

    def unload(self) -> dict:
        return {"row": self.row, "col": self.col, "name": self.name}

    def update(self) -> None:
        pass

    def render(self, screen: pygame.Surface, camera: Camera) -> None:
        pos = camera.world_to_relative(
            (self.col * TILE_SIZE, self.row * TILE_SIZE))
        screen.blit(pygame.transform.scale(
            self.image, (round(TILE_SIZE * camera.zoom), round(TILE_SIZE * camera.zoom))), pos)
