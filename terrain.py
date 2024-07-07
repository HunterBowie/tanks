from __future__ import annotations

import json
from dataclasses import dataclass
from os import path

import pygame

from asset_manager import AssetManager
from camera import Camera
from constants import TERRAIN_DIR, TILE_SIZE


class Terrain:
    """The background where the tanks fight (including only tiles and imovable objects)."""

    def __init__(self, terrain_data: dict, assets: AssetManager) -> None:
        self.tiles = [Tile.load(tile, assets)
                      for tile in terrain_data["tiles"]]
        self.objects = [Obj.load(tile, assets)
                        for tile in terrain_data["objects"]]
        self.void_tiles = [
            tile for tile in self.tiles if tile.name == "void"]
        self.assets = assets

    def get_size(self) -> tuple[int, int]:
        max_row = 0
        max_col = 0
        for tile in self.tiles:
            if tile.row > max_row:
                max_row = tile.row
            if tile.col > max_col:
                max_col = tile.col
        return (max_col + 1) * TILE_SIZE, (max_row + 1) * TILE_SIZE

    def clear(self) -> None:
        self.tiles = []
        self.objects = []

    def get_data(self) -> dict:
        raw_tiles = [tile.unload() for tile in self.tiles]
        raw_objects = [obj.unload() for obj in self.objects]
        return {"tiles": raw_tiles, "objects": raw_objects}

    def add_tile(self, new_tile: dict) -> None:
        for tile in self.tiles:
            if tile.row == new_tile.row and tile.col == new_tile.col:
                self.tiles.remove(tile)
                break
        self.tiles.append(new_tile)
        if tile.name == "void":
            self.void_tiles.append(tile)

    def get_tile(self, row: int, col: int) -> dict:
        for tile in self.tiles:
            if tile.row == row and tile.col == col:
                return tile

    def render(self, screen: pygame.Surface, camera: Camera) -> None:
        for tile in self.tiles:
            pos = camera.world_to_relative(
                (tile.col * TILE_SIZE, tile.row * TILE_SIZE))
            screen.blit(pygame.transform.scale(
                tile.image, (round(TILE_SIZE * camera.zoom), round(TILE_SIZE * camera.zoom))), pos)

        for obj in self.objects:
            pos = camera.world_to_relative((obj.x, obj.y))
            screen.blit(pygame.transform.scale(obj.image, (int(obj.image.get_width(
            ) * camera.zoom), int(obj.image.get_height() * camera.zoom))), pos)
