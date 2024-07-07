
import math

import pygame
import pygame_util as util

from asset_manager import AssetManager
from camera import Camera
from constants import SCREEN_SIZE, TILE_SIZE
from world import Tank, World

pygame.init()

assets = AssetManager()
window = util.Window(SCREEN_SIZE, 'Tanks')

assets.load_images()

window.set_icon(assets.images['icon'])

world = World.load("meadows", assets)
tank = Tank(world.spawn, assets.images.tanks["tank_blue"])
camera = Camera(world.spawn)
world.add_tank(tank)


def move_tank(x_change: int, y_change: int) -> None:
    radians = math.atan2(-y_change, x_change)
    angle = math.degrees(radians)
    tank.move(angle)


running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.MOUSEBUTTONDOWN:
            (pygame.mouse.get_pos())

    keys = pygame.key.get_pressed()
    x_change, y_change = 0, 0
    if keys[pygame.K_LEFT] or keys[pygame.K_a]:
        x_change = -10
    if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
        x_change = 10
    if keys[pygame.K_UP] or keys[pygame.K_w]:
        y_change = -10
    if keys[pygame.K_DOWN] or keys[pygame.K_s]:
        y_change = 10
    if x_change != 0 or y_change != 0:
        move_tank(x_change, y_change)
    camera_x, camera_y = camera.center
    camera_dx = (tank.rect.center[0] - camera_x)
    camera_dy = (tank.rect.center[1] - camera_y)
    camera_dx *= 0.01
    camera_dy *= 0.02
    camera.move(camera_dx, 0)
    for tile in world.void_tiles:
        if tile.get_rel_rect(camera).colliderect(pygame.Rect(0, 0, window.screen.get_width(), window.screen.get_height())):
            camera.move(-camera_dx, 0)
    camera.move(0, camera_dy)
    for tile in world.void_tiles:
        if tile.get_rel_rect(camera).colliderect(pygame.Rect(0, 0, window.screen.get_width(), window.screen.get_height())):
            camera.move(0, -camera_dy)

    world.render(window.screen, camera)
    window.update()
