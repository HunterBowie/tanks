# autopep8: off

import math

import pygame
import pygame_util as util

from camera import Camera
from constants import SCREEN_SIZE, TILE_SIZE

pygame.init()

window = util.Window(SCREEN_SIZE, 'Tanks')

from assets import assets
from world import Tank, World
from world.tanks.rotation import get_angle
from world.tanks.turret import Turret

# autopep8: on

window.set_icon(assets.images['icon'])

camera = Camera()
world = World.load("meadows", camera)

camera.set_pos(world.spawn)
camera.set_barrier_rects(world.get_barrier_rects())

tank = Tank(world.spawn, camera)
world.spawn_tank(tank)

enemy_tank = Tank(world.spawn, camera)
world.spawn_tank(enemy_tank)

turret = Turret(world.spawn, camera)

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.MOUSEBUTTONDOWN:
            world.tank_fire(tank)

    keys = pygame.key.get_pressed()
    x_change, y_change = 0, 0
    if keys[pygame.K_LEFT] or keys[pygame.K_a]:
        x_change = -1
    if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
        x_change = 1
    if keys[pygame.K_UP] or keys[pygame.K_w]:
        y_change = -1
    if keys[pygame.K_DOWN] or keys[pygame.K_s]:
        y_change = 1
    if x_change != 0 or y_change != 0:
        angle = math.degrees(math.atan2(-y_change, x_change))
        world.move_tank(tank, angle)
    camera.move_with_delay_within_barriers(tank.rect.center)
    if pygame.mouse.get_focused():
        tank.turret.rotate(get_angle(camera.world_to_relative(
            tank.rect.center), pygame.mouse.get_pos()))
    world.update()
    world.render(window.screen)
    pygame.draw.circle(window.screen, util.Color.RED,
                       camera.world_to_relative(world.spawn), 5)
    window.update()
