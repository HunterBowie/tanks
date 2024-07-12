
from __future__ import annotations

import json
from dataclasses import dataclass
from os import path
from typing import Protocol

import pygame

from assets import assets
from camera import Camera
from constants import TILE_SIZE, WORLDS_DIR
from world.effects import Effect, Explosion, TrackEffect
from world.tanks import Tank
from world.world_entity import WorldEntity

from .item import Item
from .object import Object
from .tanks.bullet import Bullet
from .tile import Tile


@dataclass
class World:
    name: str
    spawn: tuple[int, int]

    tiles: list[Tile]
    physical_objects: list[Object]
    visual_objects: list[Object]
    items: list[Item]

    tanks: list[Tank]
    bullets: list[Bullet]
    effects: list[Effect]

    camera: Camera

    def __post_init__(self) -> None:
        max_row = max_col = 0
        for tile in self.tiles:
            max_row = max(max_row, tile.row)
            max_col = max(max_col, tile.col)
        self.rect = pygame.Rect(0, 0, max_col*TILE_SIZE, max_row*TILE_SIZE)

    @property
    def entities(self) -> list[WorldEntity]:
        return self.tiles + self.physical_objects + self.visual_objects + self.items + self.tanks + self.bullets + self.effects

    def get_barrier_rects(self) -> list[pygame.Rect]:
        return [tile.get_world_rect() for tile in self.tiles if tile.name == "barrier"]

    def spawn_tank(self, tank: Tank) -> None:
        self.tanks.append(tank)

    def tank_fire(self, tank: Tank) -> None:
        self.bullets.extend(tank.fire())

    def move_tank(self, tank: Tank, angle: int) -> None:
        tank.move(angle)
        if tank.track_timer.passed(2):
            self.spawn_effect(TrackEffect(tank, self.camera))
            tank.track_timer.start()

    def spawn_effect(self, effect: Effect) -> None:
        self.effects.append(effect)

    def create_explosion(self, pos: tuple[int, int]) -> None:
        self.effects.append(Explosion(pos, self.camera))

    def update(self) -> None:
        for entity in self.entities:
            entity.update()

        for effect in self.effects:
            if effect.is_dead():
                self.effects.remove(effect)

        for bullet in self.bullets:
            if not bullet.rect.colliderect(self.rect):
                self.bullets.remove(bullet)
            elif bullet.explosion_timer.passed(1):
                self.bullets.remove(bullet)
                self.create_explosion(bullet.rect.center)
            elif bullet.explosion_timer.passed(.2):
                for tank in self.tanks:
                    if tank.rect.colliderect(bullet.rect):
                        self.bullets.remove(bullet)
                        self.create_explosion(bullet.rect.center)

    def render(self, screen: pygame.Surface) -> None:
        first_layer = self.tiles
        second_layer = self.physical_objects + \
            self.visual_objects + self.items + self.effects
        third_layer = self.tanks + self.bullets
        fourth_layer = []
        for entity in first_layer:
            entity.render(screen)
        for entity in second_layer:
            entity.render(screen)
        for entity in third_layer:
            entity.render(screen)
        for entity in fourth_layer:
            entity.render(screen)

    @staticmethod
    def load(world_name: str, camera: Camera) -> World:
        file_path = path.join(WORLDS_DIR, world_name + ".json")
        with open(file_path, "r") as file:
            data = json.load(file)
            spawn = tuple(data["spawn"])
            tiles = [Tile.load(tile, camera) for tile in data["tiles"]]
            physical_objects = [Object.load(object, camera)
                                for object in data["physical_objects"]]
            visual_objects = [Object.load(object, camera)
                              for object in data["visual_objects"]]
            items = [Item.load(item, camera) for item in data["items"]]

            return World(world_name, spawn, tiles, physical_objects, visual_objects, items, [], [], [], camera)


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
