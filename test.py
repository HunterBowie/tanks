import pygame
import pygame_util as util

from constants import SCREEN_SIZE

window = util.Window(SCREEN_SIZE)
run = True
while run:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            print(event.button)

    window.update()
