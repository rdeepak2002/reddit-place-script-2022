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


def test_generate_rgb_colors_array_ok():
    assert ColorMapper.generate_rgb_colors_array() == [
        (190, 0, 57),
        (255, 69, 0),
        (255, 168, 0),
        (255, 214, 53),
        (0, 163, 104),
        (0, 204, 120),
        (126, 237, 86),
        (0, 117, 111),
        (0, 158, 170),
        (36, 80, 164),
        (54, 144, 234),
        (81, 233, 244),
        (73, 58, 193),
        (106, 92, 255),
        (129, 30, 159),
        (180, 74, 192),
        (255, 56, 129),
        (255, 153, 170),
        (109, 72, 47),
        (156, 105, 38),
        (0, 0, 0),
        (137, 141, 144),
        (212, 215, 217),
        (255, 255, 255)
    ]
