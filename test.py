from math import cos, radians, sin

import pygame
import pygame_util as util

window = util.Window((500, 500))


center_point = 250, 250
other_point = 300, 300
original_other_point = other_point

angle = 0

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            angle += 10
            offset = original_other_point[0] - \
                center_point[0], -(original_other_point[1]-center_point[1])
            x = offset[0]*cos(radians(angle)) - \
                offset[1]*sin(radians(angle))
            y = offset[0]*sin(radians(angle)) + \
                offset[1]*cos(radians(angle))
            print(x, y)
            other_point = x+center_point[0], -y+center_point[1]

    pygame.draw.circle(window.screen, util.Color.RED, center_point, 5)
    pygame.draw.circle(window.screen, util.Color.GREEN, other_point, 5)

    window.update()
