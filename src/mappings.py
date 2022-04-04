import math
from PIL import ImageColor


class ColorMapper:
    COLOR_MAP = {
        "#6D001A": 0,  # darkest red
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
        "#00CCC0": 11,  # light teal
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
        "#515252": 28,  # dark gray
        "#898D90": 29,  # gray
        "#D4D7D9": 30,  # light gray
        "#FFFFFF": 31,  # white
    }

    # map of pixel color ids to verbose name (for debugging)
    NAME_MAP = {
        0: "Darkest Red",
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
        if color_id in ColorMapper.NAME_MAP.keys():
            return "{} ({})".format(ColorMapper.NAME_MAP[color_id], str(color_id))
        return "Invalid Color ({})".format(str(color_id))

    @staticmethod
    def closest_color(
        target_rgb: tuple, rgb_colors_array: list, legacy_transparency: bool
    ):
        """Find the closest rgb color from palette to a target rgb color, as well as handling transparency"""

        # first check is for the alpha channel transparency in ex. png
        if target_rgb[3] == 0:
            return (69, 42, 0)
        # second check is for the legacy method of transparency using hex #452A00.
        if target_rgb[:3] == (69, 42, 0) and legacy_transparency:
            return (69, 42, 0)

        r, g, b = target_rgb[:3]
        color_diffs = []
        for color in rgb_colors_array:
            cr, cg, cb = color
            color_diff = math.sqrt((r - cr) ** 2 + (g - cg) ** 2 + (b - cb) ** 2)
            color_diffs.append((color_diff, color))
        return min(color_diffs)[1]

    @staticmethod
    def generate_rgb_colors_array():
        """Generate array of available rgb colors to be used"""
        return [
            ImageColor.getcolor(color_hex, "RGB")
            for color_hex in list(ColorMapper.COLOR_MAP.keys())
        ]
