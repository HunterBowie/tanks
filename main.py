
import pygame
import pygame_util as util

from asset_manager import AssetManager
from camera import Camera
from constants import SCREEN_SIZE
from tank import Tank
from terrain import Terrain

pygame.init()

assets = AssetManager()
window = util.Window(SCREEN_SIZE, 'Tanks')

assets.load_images()

window.set_icon(assets.images['icon'])

terrain = Terrain.load("meadows")
camera = Camera(1300, 1600)

tank = Tank(1300, 1600, assets.images.objects["tankBody_blue_outline"])

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    keys = pygame.key.get_pressed()

    if keys[pygame.K_LEFT] or keys[pygame.K_a]:
        camera.move(-10, 0)
    if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
        camera.move(10, 0)
    if keys[pygame.K_UP] or keys[pygame.K_w]:
        camera.move(0, -10)
    if keys[pygame.K_DOWN] or keys[pygame.K_s]:
        camera.move(0, 10)

    terrain.render(window.screen, camera, assets)
    tank.render(window.screen, camera)

    window.update()
