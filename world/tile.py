from __future__ import annotations

from dataclasses import dataclass

import pygame

from assets import assets
from camera import Camera
from constants import TILE_SIZE


@dataclass
class Tile:
    RENDERING_LAYER = 0

    row: int
    col: int
    name: str
    image: pygame.Surface
    camera: Camera

    def get_rel_rect(self) -> pygame.Rect:
        rel_tile_size = TILE_SIZE * self.camera.zoom
        row, col = self.row, self.col
        world_pos = col * rel_tile_size, row * rel_tile_size
        rel_x, rel_y = self.camera.world_to_relative(world_pos)
        return pygame.Rect(rel_x, rel_y, rel_tile_size, rel_tile_size)

    def get_world_rect(self) -> pygame.Rect:
        world_x = self.col * TILE_SIZE
        world_y = self.row * TILE_SIZE
        return pygame.Rect(world_x, world_y, TILE_SIZE, TILE_SIZE)

    @staticmethod
    def load(data: dict, camera: Camera) -> Tile:
        return Tile(data["row"], data["col"], data["name"], assets.images.tiles[data["name"]], camera)

    def unload(self) -> dict:
        return {"row": self.row, "col": self.col, "name": self.name}

    def update(self) -> None:
        pass

    def render(self, screen: pygame.Surface) -> None:
        rect = self.get_world_rect()
        if rect.colliderect(self.camera.rect):
            rect = self.get_rel_rect()
            if self.camera.zoom != 1:
                rect.topleft = self.camera.world_to_relative(
                    (self.col * TILE_SIZE, self.row * TILE_SIZE))
            screen.blit(pygame.transform.scale(
                self.image, (round(TILE_SIZE * self.camera.zoom), round(TILE_SIZE * self.camera.zoom))), rect.topleft)
