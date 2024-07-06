from __future__ import annotations

import json
from os import path

import pygame

from asset_manager import AssetManager
from camera import Camera
from constants import TERRAIN_DIRECTORY, TILE_SIZE


class Terrain:
    """The background where the tanks fight."""

    def __init__(self, data: dict, name: str) -> None:
        self.name = name
        self.tiles = data["tiles"]
        self.objects = data["objects"]

    def clear(self) -> None:
        self.tiles = []
        self.objects = []

    def get_data(self) -> dict:
        max_row = 0
        max_col = 0
        for tile in self.tiles:
            if tile["row"] > max_row:
                max_row = tile["row"]
            if tile["col"] > max_col:
                max_col = tile["col"]
        width = (max_col + 1) * TILE_SIZE
        height = (max_row + 1) * TILE_SIZE
        return {"size": [width, height], "tiles": self.tiles, "objects": self.objects}

    def add_tile(self, new_tile: dict) -> None:
        for tile in self.tiles:
            if tile["row"] == new_tile["row"] and tile["col"] == new_tile["col"]:
                self.tiles.remove(tile)
                break
        self.tiles.append(new_tile)

    def get_tile(self, row: int, col: int) -> dict:
        for tile in self.tiles:
            if tile["row"] == row and tile["col"] == col:
                return tile

    @staticmethod
    def load(name: str) -> Terrain:
        file_path = path.join(TERRAIN_DIRECTORY, name + ".json")
        with open(file_path, "r") as file:
            return Terrain(json.load(file), name)

    def save(self) -> None:
        file_path = path.join(TERRAIN_DIRECTORY, self.name + ".json")
        with open(file_path, "w") as file:
            json.dump(self.get_data(), file, indent=4)

    def render(self, screen: pygame.Surface, camera: Camera, assets: AssetManager) -> None:
        for tile in self.tiles:
            tile_name = tile['name']
            tile_image = assets.images.tiles[tile_name]

            pos = camera.world_to_relative(
                (tile['col'] * TILE_SIZE, tile['row'] * TILE_SIZE))
            screen.blit(pygame.transform.scale(
                tile_image, (round(TILE_SIZE * camera.zoom), round(TILE_SIZE * camera.zoom))), pos)

        for obj in self.objects:
            obj_image = assets.images.objects[obj['name']]
            pos = camera.world_to_relative((obj['x'], obj['y']))
            screen.blit(pygame.transform.scale(obj_image, (int(obj_image.get_width(
            ) * camera.zoom), int(obj_image.get_height() * camera.zoom))), pos)
