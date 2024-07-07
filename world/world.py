
from __future__ import annotations

import json
from dataclasses import dataclass
from os import path
from typing import Protocol

import pygame

from asset_manager import AssetManager
from camera import Camera
from constants import WORLDS_DIR
from world.tanks import Tank

from .effect import Effect
from .item import Item
from .object import Object
from .tanks.missile import Missile
from .tile import Tile


class WorldEntity(Protocol):
    def update(self) -> None:
        ...

    def render(self, screen: pygame.Surface, camera: Camera) -> None:
        ...


@dataclass
class World:
    name: str
    spawn: tuple[int, int]

    tiles: list[Tile]
    physical_objects: list[Object]
    visual_objects: list[Object]
    items: list[Item]

    tanks: list[Tank]
    missiles: list[Missile]
    effects: list[Effect]

    def __post_init__(self) -> None:
        self.entities: list[WorldEntity] = self.tiles + self.physical_objects + \
            self.visual_objects + self.tanks + self.missiles + self.items + self.effects
        self.void_tiles = [tile for tile in self.tiles if tile.name == "void"]

    def add_tank(self, tank: Tank) -> None:
        self.tanks.append(tank)
        self.entities.append(tank)

    def update(self) -> None:
        for entity in self.entities:
            entity.update()

    def render(self, screen: pygame.Surface, camera: Camera) -> None:
        first_layer = self.tiles
        second_layer = self.physical_objects + self.visual_objects + self.items
        third_layer = self.tanks + self.missiles
        fourth_layer = self.effects
        for entity in first_layer:
            entity.render(screen, camera)
        for entity in second_layer:
            entity.render(screen, camera)
        for entity in third_layer:
            entity.render(screen, camera)
        for entity in fourth_layer:
            entity.render(screen, camera)

    @staticmethod
    def load(world_name: str, assets: AssetManager) -> World:
        file_path = path.join(WORLDS_DIR, world_name + ".json")
        with open(file_path, "r") as file:
            data = json.load(file)
            spawn = tuple(data["spawn"])
            tiles = [Tile.load(tile, assets) for tile in data["tiles"]]
            physical_objects = [Object.load(object, assets)
                                for object in data["physical_objects"]]
            visual_objects = [Object.load(object, assets)
                              for object in data["visual_objects"]]
            items = [Item.load(item, assets) for item in data["items"]]

            return World(world_name, spawn, tiles, physical_objects, visual_objects, items, [], [], [])


@dataclass
class MakerWorld(World):
    def _get_data(self) -> dict:
        raw_tiles = [tile.unload() for tile in self.tiles]
        raw_physical_objects = [object.unload()
                                for object in self.physical_objects]
        raw_visual_objects = [object.unload()
                              for object in self.visual_objects]
        raw_items = [item.unload() for item in self.items]
        return {"spawn": list(self.spawn), "tiles": raw_tiles, "physical_objects": raw_physical_objects, "visual_objects": raw_visual_objects, "items": raw_items}

    def save(self) -> None:
        file_path = path.join(WORLDS_DIR, self.name + ".json")
        with open(file_path, "w") as file:
            json.dump(self._get_data(), file, indent=4)

    def get_tile(self, row, col) -> Tile:
        for tile in self.tiles:
            if tile.row == row and tile.col == col:
                return tile
        return None

    def add_tile(self, new_tile: Tile) -> None:
        for tile in self.tiles:
            if tile.row == new_tile.row and tile.col == new_tile.col:
                self.tiles.remove(tile)
                self.entities.remove(tile)
        self.tiles.append(new_tile)
        self.entities.append(new_tile)

    def remove_tile(self, tile: Tile) -> None:
        self.tiles.remove(tile)
        self.entities.remove(tile)

    @staticmethod
    def load(world_name: str, assets: AssetManager) -> World:
        world = World.load(world_name, assets)
        return MakerWorld(world.name, world.spawn, world.tiles, world.physical_objects, world.visual_objects, world.items, [], [], [])
