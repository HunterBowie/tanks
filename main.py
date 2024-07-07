
import pygame
import pygame_util as util

from asset_manager import AssetManager
from camera import Camera
from constants import SCREEN_SIZE, TILE_SIZE
from tank import Tank
from terrain import Terrain
from world import World

pygame.init()

assets = AssetManager()
window = util.Window(SCREEN_SIZE, 'Tanks')

assets.load_images()

window.set_icon(assets.images['icon'])

world = World("meadows", assets)
camera = Camera(world.spawn)


def move_camera(x_change: int, y_change: int) -> None:
    camera.move(x_change, y_change)
    for tile in world.terrain.void_tiles:
        if tile.get_rel_rect(camera).colliderect(pygame.Rect(0, 0, window.screen.get_width(), window.screen.get_height())):
            camera.move(-x_change, -y_change)


running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    keys = pygame.key.get_pressed()

    if keys[pygame.K_LEFT] or keys[pygame.K_a]:
        move_camera(-10, 0)
    if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
        move_camera(10, 0)
    if keys[pygame.K_UP] or keys[pygame.K_w]:
        move_camera(0, -10)
    if keys[pygame.K_DOWN] or keys[pygame.K_s]:
        move_camera(0, 10)

    world.render(window.screen, camera)
    window.update()
