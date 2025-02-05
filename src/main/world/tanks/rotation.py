"""A collection of useful function about rotation and angles."""

import math

import pygame


def move_pos_with_degrees(pos: tuple[int, int], angle: int, speed: float) -> tuple[int, int]:
    """Move a position in the direction of an angle."""
    radians = math.radians(angle)
    x = round(pos[0] + speed * math.cos(radians))
    y = round(pos[1] - speed * math.sin(radians))
    return x, y


def move_rect_with_degrees(rect: pygame.Rect, angle: int, speed: float) -> None:
    """Move a rect in the direction of an angle."""
    rect.topleft = move_pos_with_degrees(rect.topleft, angle, speed)


def get_angle(start: tuple[int, int], end: tuple[int, int]) -> int:
    """Get the angle between two points from the perspective of the first point."""
    radians = math.atan2(-(end[1]-start[1]), (end[0]-start[0]))
    return math.degrees(radians)


def rotate_point_around_origin(point: tuple[int, int], angle: int) -> tuple[int, int]:
    "Rotate a point in space around another point be a certain amount of degrees."
    point = point[0], -point[1]

    x = point[0]*math.cos(math.radians(angle)) - \
        point[1]*math.sin(math.radians(angle))
    y = point[0]*math.sin(math.radians(angle)) + \
        point[1]*math.cos(math.radians(angle))

    return x, -y
