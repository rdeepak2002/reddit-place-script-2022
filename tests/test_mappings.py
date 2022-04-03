import pytest
from src.mappings import (
    ColorMapper,
    InvalidColorIdException,
    InvalidRGBException,
)


@pytest.mark.parametrize("rgb, expected", [
    ((255, 255, 255), "#FFFFFF"),
    ((0, 0, 0), "#000000"),
    ((255, 0, 0), "#FF0000"),
    ((0, 255, 0), "#00FF00"),
    ((0, 0, 255), "#0000FF"),
])
def test_rgb_to_hex(rgb, expected):
    assert ColorMapper.rgb_to_hex(rgb) == expected


@pytest.fixture(params=ColorMapper.NAME_MAP.keys())
def id_name(request):
    return request.param, ColorMapper.NAME_MAP.get(request.param)


def test_color_id_to_name_ok(id_name):
    color_id, color_name = id_name
    assert ColorMapper.color_id_to_name(color_id) == f"{color_name} ({color_id})"


def test_color_id_to_name_failure():
    with pytest.raises(InvalidColorIdException):
        ColorMapper.color_id_to_name(999)


@pytest.mark.parametrize("target_rgb, rgb_colors_array", [
    ((255, 255, 255, 0), [
        (255, 255, 255),
        (0, 0, 0),
        (255, 0, 0),
        (0, 255, 0),
        (0, 0, 255),
    ]),

])
def test_closest_color_ok(target_rgb, rgb_colors_array):
    assert ColorMapper.closest_color(
        target_rgb, rgb_colors_array) == ColorMapper.COLOR_SKIP


def test_closest_color_too_short_exception():
    with pytest.raises(InvalidRGBException):
        ColorMapper.closest_color((255, 255, 255), [255, 255, 255])


def test_closest_color_too_long_exception():
    with pytest.raises(InvalidRGBException):
        ColorMapper.closest_color((255, 255, 255, 0, 0), [(255, 255, 255)])
