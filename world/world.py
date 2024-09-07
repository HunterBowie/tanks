
from __future__ import annotations

import json
import math
from dataclasses import dataclass
from os import path

import pygame

from assets import assets
from camera import Camera
from constants import (NUM_RENDERING_LAYERS, TILE_SIZE, WORLDS_DIR, EntityType,
                       ExplosionSize)
from world.effects import Effect, ExplosionEffect, TrackEffect
from world.entity import Entity
from world.tanks import Tank

from .bullet import Bullet
from .item import Item
from .object import Object
from .tile import Tile


@dataclass
class World:
    name: str
    spawn: tuple[int, int]
    entities: dict[EntityType, list[Entity]]
    camera: Camera
    rect: pygame.Rect

    def get_barrier_rects(self) -> list[pygame.Rect]:
        return [tile.get_world_rect() for tile in self.entities[EntityType.TILE] if tile.name == "barrier"]

    def spawn_tank(self, tank: Tank) -> None:
        self.entities[EntityType.TANK].append(tank)

    def tank_fire(self, tank: Tank) -> None:
        self.entities[EntityType.BULLET].extend(tank.fire())
        assets.sounds.effects["pop"].play()

    def move_tank(self, tank: Tank, angle: int) -> None:
        tank.move(
            angle, [other_tank for other_tank in self.entities[EntityType.TANK] if tank != other_tank])

        if tank.track_timer.passed(2):
            self.entities[EntityType.EFFECT].append(
                TrackEffect(tank, self.camera))
            tank.track_timer.start()

    def create_explosion(self, pos: tuple[int, int], explosion_size: ExplosionSize) -> None:
        self.entities[EntityType.EFFECT].append(
            ExplosionEffect(pos, explosion_size, self.camera))
        assets.sounds.effects["explosion"].play()

    def _update_bullet_seeking(self, bullet: Bullet) -> None:
        if bullet.seeking_target_id == -1:
            if not bullet.seeking_timer.passed(.100):
                return
            tanks: list[Tank] = self.entities[EntityType.TANK].copy()
            for tank in tanks:
                if tank.id == bullet.tank_id:
                    tanks.remove(tank)
            distances = [math.dist(tank.rect.center, bullet.rect.center)
                         for tank in tanks]
            min_dist = min(distances)
            if min_dist > bullet.seeking_radius:
                bullet.seeking_timer.start()
                return
            tank = tanks[distances.index(min(distances))]
            bullet.seeking_target_id = tank.id

        for tank in self.entities[EntityType.TANK]:
            if tank.id == bullet.seeking_target_id:
                dist = math.dist(bullet.rect.center, tank.rect.center)
                if dist > bullet.seeking_radius:
                    bullet.seeking_target_id = -1
                    bullet.seeking_timer.start()
                    return
                x_change = tank.rect.centerx-bullet.rect.centerx
                y_change = tank.rect.centery-bullet.rect.centery
                angle = math.degrees(math.atan2(-y_change, x_change))
                if angle < 0:
                    angle += 360
                angle_change = angle-bullet.angle
                if angle_change > 180:
                    angle_change -= 360
                bullet.rotate(bullet.angle + angle_change*bullet.seeking_force)
                break
        else:
            bullet.seeking_target_id = -1
            bullet.seeking_timer.start()

    def update(self) -> None:
        for entities in self.entities.values():
            for entity in entities:
                entity.update()

        self.entities[EntityType.EFFECT] = [
            effect for effect in self.entities[EntityType.EFFECT] if not effect.is_finished()]

        for bullet in self.entities[EntityType.BULLET]:
            if not bullet.rect.colliderect(self.rect):
                self.entities[EntityType.BULLET].remove(bullet)
            else:
                if bullet.seeking_force > 0:
                    self._update_bullet_seeking(bullet)
                for tank in self.entities[EntityType.TANK]:
                    if tank.id != bullet.tank_id:
                        if tank.rect.colliderect(bullet.rect):
                            self.entities[EntityType.BULLET].remove(bullet)
                            self.create_explosion(
                                bullet.rect.center, bullet.explosion_size)
                            break

    def render(self, screen: pygame.Surface) -> None:
        layers: list[list[Entity]] = [[] for i in range(NUM_RENDERING_LAYERS)]
        for entities in self.entities.values():
            for entity in entities:
                layers[entity.RENDERING_LAYER].append(entity)

        for layer in layers:
            for entity in layer:
                entity.render(screen)

    @staticmethod
    def load(world_name: str, camera: Camera) -> World:
        file_path = path.join(WORLDS_DIR, world_name + ".json")
        with open(file_path, "r") as file:
            data = json.load(file)

            spawn = tuple(data["spawn"])

            tiles = [Tile.load(tile, camera) for tile in data["tiles"]]
            objects = [Object.load(object, camera)
                       for object in data["objects"]]
            items = [Item.load(item, camera) for item in data["items"]]

            entities = {
                EntityType.TILE: tiles, EntityType.OBJECT: objects,
                EntityType.ITEM: items, EntityType.EFFECT: [],
                EntityType.BULLET: [], EntityType.TANK: []
            }

            max_row = max_col = 0
            for tile in tiles:
                max_row = max(max_row, tile.row)
                max_col = max(max_col, tile.col)
            rect = pygame.Rect(0, 0, max_col*TILE_SIZE, max_row*TILE_SIZE)

            return World(world_name, spawn, entities, camera, rect)


@dataclass
class MakerWorld(World):
    def _get_data(self) -> dict:
        raw_tiles = [tile.unload() for tile in self.entities[EntityType.TILE]]
        raw_objects = [object.unload()
                       for object in self.entities[EntityType.OBJECT]]
        raw_items = [item.unload() for item in self.entities[EntityType.ITEM]]
        return {"spawn": list(self.spawn), "tiles": raw_tiles, "objects": raw_objects, "items": raw_items}

    def save(self) -> None:
        file_path = path.join(WORLDS_DIR, self.name + ".json")
        with open(file_path, "w") as file:
            json.dump(self._get_data(), file, indent=4)

    def get_tile(self, row, col) -> Tile:
        for tile in self.entities[EntityType.TILE]:
            if tile.row == row and tile.col == col:
                return tile
        return None

    def add_tile(self, new_tile: Tile) -> None:
        for tile in self.entities[EntityType.TILE]:
            if tile.row == new_tile.row and tile.col == new_tile.col:
                self.entities[EntityType.TILE].remove(tile)
        self.entities[EntityType.TILE].append(new_tile)

    def remove_tile(self, tile: Tile) -> None:
        self.entities[EntityType.TILE].remove(tile)

    @staticmethod
    def load(world_name: str, camera: Camera) -> World:
        world = World.load(world_name, camera)
        return MakerWorld(world.name, world.spawn, world.entities, world.camera, world.rect)
