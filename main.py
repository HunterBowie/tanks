# autopep8: off

import math

import pygame
import pygame_util as util

from camera import Camera
from constants import SCREEN_SIZE, TankColor, TurretType

pygame.init()

window = util.Window(SCREEN_SIZE, 'Tanks')

from assets import assets
from world import BasicTank, BeastTank, BlitzTank, SeekingTank, Tank, World
from world.tanks.rotation import get_angle

# autopep8: on

window.set_icon(assets.images['icon'])

camera = Camera()
world = World.load("meadows", camera)

camera.set_pos(world.spawn)
camera.set_barrier_rects(world.get_barrier_rects())

tank1 = BasicTank(world.spawn, TurretType.WIDE, TankColor.BLUE, camera)
world.spawn_tank(tank1)

x, y = world.spawn
x += 100
tank2 = BasicTank((x, y), TurretType.BARREL, TankColor.RED, camera)
world.spawn_tank(tank2)

x += 100
tank3 = SeekingTank((x, y), camera)
world.spawn_tank(tank3)

x += 125
tank4 = BlitzTank((x, y), camera)
world.spawn_tank(tank4)

tanks: list[Tank] = [tank1, tank2, tank3, tank4]
index = 1
tank = tank1

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                tank = tanks[index]
                index += 1
                if index > 3:
                    index = 0

    pressed = pygame.mouse.get_pressed()
    if pressed[0] and tank.firing_cooldown_reached():
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
        if angle < 0:
            angle += 360
        world.move_tank(tank, angle)
    camera.move_with_delay_within_barriers(tank.rect.center)
    if pygame.mouse.get_focused():
        for turret in tank.turrets:
            turret.rotate(get_angle(camera.world_to_relative(
                tank.rect.center), pygame.mouse.get_pos()))
    world.update()
    world.render(window.screen)
    # for other_tank in tanks:
    #     if other_tank != tank:
    #         other_tank.render_health_bar(window.screen)
    window.update()
