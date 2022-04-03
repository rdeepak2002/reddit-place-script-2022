import math
from PIL import ImageColor
from loguru import logger


class InvalidColorIdException(Exception):
    def __init__(self, color_id: str):
        self.message = f"Invalid ColorId: {color_id}"


class InvalidRGBException(Exception):
    def __init__(self, rgb: tuple):
        self.message = f"Invalid RGB: {rgb}"


class ColorMapper:
    COLOR_SKIP = (69, 42, 0)

    COLOR_MAP = {
        "#6D001A": 0,  # Darkest red
        "#BE0039": 1,  # dark red
        "#FF4500": 2,  # red
        "#FFA800": 3,  # orange
        "#FFD635": 4,  # yellow
        "#FFF8B8": 5,  # pale yellow
        "#00A368": 6,  # dark green
        "#00CC78": 7,  # green
        "#7EED56": 8,  # light green
        "#00756F": 9,  # dark teal
        "#009EAA": 10,  # teal
        "#00CC00": 11,  # light teal
        "#2450A4": 12,  # dark blue
        "#3690EA": 13,  # blue
        "#51E9F4": 14,  # light blue
        "#493AC1": 15,  # indigo
        "#6A5CFF": 16,  # periwinkle
        "#94B3FF": 17,  # lavender
        "#811E9F": 18,  # dark purple
        "#B44AC0": 19,  # purple
        "#E4ABFF": 20,  # pale purple
        "#DE107F": 21,  # magenta
        "#FF3881": 22,  # pink
        "#FF99AA": 23,  # light pink
        "#6D482F": 24,  # dark brown
        "#9C6926": 25,  # brown
        "#FFB470": 26,  # beige
        "#000000": 27,  # black
        "#515252": 28,  # Dark gray
        "#898D90": 29,  # gray
        "#D4D7D9": 30,  # light gray
        "#FFFFFF": 31,  # white
    }

    # map of pixel color ids to verbose name (for debugging)
    NAME_MAP = {
        1: "Dark Red",
        2: "Bright Red",
        3: "Orange",
        4: "Yellow",
        5: "Pale yellow",
        6: "Dark Green",
        7: "Green",
        8: "Light Green",
        9: "Dark Teal",
        10: "Teal",
        11: "Light Teal",
        12: "Dark Blue",
        13: "Blue",
        14: "Light Blue",
        15: "Indigo",
        16: "Periwinkle",
        17: "Lavender",
        18: "Dark Purple",
        19: "Purple",
        20: "pale purple",
        21: "magenta",
        22: "Pink",
        23: "Light Pink",
        24: "Dark Brown",
        25: "Brown",
        26: "beige",
        27: "Black",
        28: "dark gray",
        29: "Gray",
        30: "Light Gray",
        31: "White",
    }

    @staticmethod
    def rgb_to_hex(rgb: tuple):
        """Convert rgb tuple to hexadecimal string."""
        return ("#%02x%02x%02x" % rgb).upper()

    @staticmethod
    def color_id_to_name(color_id: int):
        """More verbose color indicator from a pixel color id."""
        if color_id not in ColorMapper.NAME_MAP.keys():
            logger.error(f"Unknown color id: {color_id}")
            raise InvalidColorIdException(color_id)

        return f"{ColorMapper.NAME_MAP[color_id]} ({color_id})"

    @staticmethod
    def closest_color(target_rgb: tuple, rgb_colors_array: list):
        """Find the closest rgb color from palette to a target rgb color"""
        if len(target_rgb) != 4:
            raise InvalidRGBException(target_rgb)

        target_red, target_green, target_blue = target_rgb[:3]

        if target_rgb[3] != 0:
            color_diffs = []
            for color in rgb_colors_array:
                color_red, color_green, color_blue = color
                curr_diff = math.sqrt(
                    (target_red - color_red) ** 2 +
                    (target_green - color_green) ** 2 +
                    (target_blue - color_blue) ** 2
                )
                color_diffs.append((curr_diff, color))

            return min(color_diffs)[1]

        return ColorMapper.COLOR_SKIP

    @staticmethod
    def generate_rgb_colors_array():
        """Generate array of available rgb colors to be used"""
        colors = []

        for hex in ColorMapper.COLOR_MAP.keys():
            colors.append(ImageColor.getrgb(hex))

        return colors
