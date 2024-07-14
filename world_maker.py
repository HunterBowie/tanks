# autopep8: off

import json
import os

import pygame
import pygame_util as util

from constants import SCREEN_SIZE, TILE_SIZE, MouseButton

pygame.init()

window = util.Window(SCREEN_SIZE, "Map Maker", max_fps=100)

from assets import assets
from camera import Camera
from world import MakerWorld, Tile

# autopep8: on


window.set_icon(assets.images.ui["wrench"])


camera = Camera()
world: MakerWorld = MakerWorld.load("dunes", camera)

camera.set_barrier_rects([])
camera.set_pos(world.spawn)


def get_mouse_row_col() -> tuple[int, int]:
    world_x, world_y = camera.relative_to_world(pygame.mouse.get_pos())
    col = world_x//TILE_SIZE
    row = world_y//TILE_SIZE
    return row, col


def main():
    running = True
    screen = window.screen
    current_tile_index = 0
    tiles = list(assets.images.tiles.keys())

    filling_area = False
    fill_start_row_col = 0, 0

    while running:
        keys = pygame.key.get_pressed()
        mouse_buttons = pygame.mouse.get_pressed()
        mouse_row, mouse_col = get_mouse_row_col()

        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            camera.move(-10, 0)
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            camera.move(10, 0)
        if keys[pygame.K_UP] or keys[pygame.K_w]:
            camera.move(0, -10)
        if keys[pygame.K_DOWN] or keys[pygame.K_s]:
            camera.move(0, 10)

        if mouse_buttons[MouseButton.Pressed.LEFT]:
            if mouse_row >= 0 and mouse_col >= 0:
                world.add_tile(
                    Tile.load({"row": mouse_row, "col": mouse_col, "name": tiles[current_tile_index]}, camera))

        if mouse_buttons[MouseButton.Pressed.RIGHT]:
            tile = world.get_tile(mouse_row, mouse_col)
            if tile:
                world.remove_tile(tile)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == MouseButton.Down.SCROLL_UP:
                    camera.zoom_in()
                elif event.button == MouseButton.Down.SCROLL_DOWN:
                    camera.zoom_out()
                elif event.button == MouseButton.Down.SIDE_FRONT:
                    current_tile_index += 1
                    if current_tile_index == len(tiles):
                        current_tile_index = 0
                elif event.button == MouseButton.Down.SIDE_BACK:
                    current_tile_index -= 1
                    if current_tile_index < 0:
                        current_tile_index = len(tiles)-1
                elif event.button == MouseButton.Down.MIDDLE:
                    tile = world.get_tile(mouse_row, mouse_col)
                    if tile:
                        current_tile_index = tiles.index(
                            tile["name"])

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_l:
                    world.save()

                elif event.key == pygame.K_f:
                    if mouse_row >= 0 or mouse_col >= 0:
                        fill_start_row_col = mouse_row, mouse_col
                        filling_area = True

            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_f:
                    start = fill_start_row_col
                    end = mouse_row, mouse_col
                    for row in range(start[0], end[0]):
                        for col in range(start[1], end[1]):
                            world.add_tile(
                                Tile.load({"row": row, "col": col, "name": tiles[current_tile_index]}, assets))
                    filling_area = False

        world.render(screen)

        is_mouse_focused = pygame.mouse.get_focused()
        if is_mouse_focused and mouse_row >= 0 and mouse_col >= 0:
            surface: pygame.Surface = assets.images.tiles[tiles[current_tile_index]].copy(
            )
            surface.set_alpha(100)
            if filling_area:
                start = fill_start_row_col
                end = mouse_row, mouse_col
                for row in range(start[0], end[0]):
                    for col in range(start[1], end[1]):
                        pos = camera.world_to_relative(
                            (col * TILE_SIZE, row * TILE_SIZE))
                        screen.blit(pygame.transform.scale(
                            surface, (round(TILE_SIZE * camera.zoom), round(TILE_SIZE * camera.zoom))), pos)
            else:
                pos = camera.world_to_relative(
                    (mouse_col * TILE_SIZE, mouse_row * TILE_SIZE))
                screen.blit(pygame.transform.scale(
                    surface, (round(TILE_SIZE * camera.zoom), round(TILE_SIZE * camera.zoom))), pos)

        window.update()

    pygame.quit()


if __name__ == "__main__":
    main()
