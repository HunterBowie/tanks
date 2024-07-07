
from __future__ import annotations

import json
from dataclasses import dataclass
from os import path
from typing import Protocol

import pygame

from asset_manager import AssetManager
from camera import Camera
from constants import WORLDS_DIR
from tank import Tank

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

    def update(self) -> None:
        for entity in self.entities:
            entity.update()

    def render(self, screen: pygame.Surface, camera: Camera) -> None:
        for entity in self.entities:
            entity.render(screen, camera)

    @staticmethod
    def load(world_name: str, assets: AssetManager) -> World:
        file_path = path.join(WORLDS_DIR, world_name + ".json")
        with open(file_path, "r") as file:
            data = json.load(file_path)
            tiles = [Tile.load(tile, assets) for tile in data["tiles"]]
            physical_objects = [Object.load(object, assets)
                                for object in data["physical_objects"]]
            visual_objects = [Object.load(object, assets)
                              for object in data["visual_objects"]]
            items = [Item.load(item, assets) for item in data["items"]]

            return World(tiles, physical_objects, visual_objects, items, [], [], [])
