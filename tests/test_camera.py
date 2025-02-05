import pygame
import pytest

from camera import Camera


@pytest.fixture
def test_camera() -> Camera:
    return Camera(pygame.Rect(100, 100, 50, 50))


def test_world_to_relative_lower_right(test_camera):
    assert test_camera.world_to_relative((150, 150)) == (50, 50)


def test_world_to_relative_upper_left(test_camera):
    assert test_camera.world_to_relative((100, 100)) == (0, 0)


def test_world_to_relative_middle(test_camera):
    assert test_camera.world_to_relative((125, 125)) == (25, 25)


def test_relative_to_world_lower_right(test_camera):
    assert test_camera.relative_to_world((50, 50)) == (150, 150)


def test_relative_to_world_upper_left(test_camera):
    assert test_camera.relative_to_world((0, 0)) == (100, 100)


def test_relative_to_world_middle(test_camera):
    assert test_camera.relative_to_world((25, 25)) == (125, 125)


@pytest.fixture
def zoomed_test_camera() -> Camera:
    camera = Camera(pygame.Rect(100, 100, 50, 50))
    camera.zoom_in()
    return camera


def test_world_to_relative_lower_right_zoom(zoomed_test_camera):
    assert zoomed_test_camera.world_to_relative(
        (125, 125)) == (round((50 / 1.2)/2), round((50 / 1.2)/2))


# def test_world_to_relative_upper_left_zoom(zoomed_test_camera):
#     assert zoomed_test_camera.world_to_relative((100, 100)) == (0, 0)


# def test_world_to_relative_middle_zoom(zoomed_test_camera):
#     assert zoomed_test_camera.world_to_relative((125, 125)) == (25, 25)


# def test_relative_to_world_lower_right_zoom(zoomed_test_camera):
#     assert zoomed_test_camera.relative_to_world((50, 50)) == (150, 150)


# def test_relative_to_world_upper_left_zoom(zoomed_test_camera):
#     assert zoomed_test_camera.relative_to_world_zoom((0, 0)) == (100, 100)


# def test_relative_to_world_middle(zoomed_test_camera):
#     assert zoomed_test_camera.relative_to_world_zoom((25, 25)) == (125, 125)
