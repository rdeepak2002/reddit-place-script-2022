import math
from PIL import ImageColor


class ColorMapper:
    COLOR_MAP = {
        "#BE0039": 1,  # dark red
        "#FF4500": 2,  # red
        "#FFA800": 3,  # orange
        "#FFD635": 4,  # yellow
        "#00A368": 6,  # dark green
        "#00CC78": 7,  # green
        "#7EED56": 8,  # light green
        "#00756F": 9,  # dark teal
        "#009EAA": 10,  # teal
        "#2450A4": 12,  # dark blue
        "#3690EA": 13,  # blue
        "#51E9F4": 14,  # light blue
        "#493AC1": 15,  # indigo
        "#6A5CFF": 16,  # periwinkle
        "#811E9F": 18,  # dark purple
        "#B44AC0": 19,  # purple
        "#FF3881": 22,  # pink
        "#FF99AA": 23,  # light pink
        "#6D482F": 24,  # dark brown
        "#9C6926": 25,  # brown
        "#000000": 27,  # black
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
        6: "Dark Green",
        7: "Green",
        8: "Light Green",
        9: "Dark Teal",
        10: "Teal",
        12: "Dark Blue",
        13: "Blue",
        14: "Light Blue",
        15: "Indigo",
        16: "Periwinkle",
        18: "Dark Purple",
        19: "Purple",
        22: "Pink",
        23: "Light Pink",
        24: "Dark Brown",
        25: "Brown",
        27: "Black",
        29: "Gray",
        30: "Light Gray",
        31: "White",
    }

    @staticmethod
    def rgb_to_hex(rgb: tuple):
        """ Convert rgb tuple to hexadecimal string. """
        return ("#%02x%02x%02x" % rgb).upper()

    @staticmethod
    def color_id_to_name(color_id: int):
        """ More verbose color indicator from a pixel color id. """
        if color_id in ColorMapper.NAME_MAP.keys():
            return "{} ({})".format(ColorMapper.NAME_MAP[color_id], str(color_id))
        return "Invalid Color ({})".format(str(color_id))

    @staticmethod
    def closest_color(target_rgb: tuple, rgb_colors_array: list):
        """ Find the closest rgb color from palette to a target rgb color"""
        r, g, b = target_rgb[:3]
        if target_rgb[3] != 0:
            color_diffs = []
            for color in self.rgb_colors_array:
                cr, cg, cb = color
                color_diff = math.sqrt((r - cr) ** 2 + (g - cg) ** 2 + (b - cb) ** 2)
                color_diffs.append((color_diff, color))
            return min(color_diffs)[1]
        else:
            return (69, 42, 0)

    @staticmethod
    def generate_rgb_colors_array():
        """ Generate array of available rgb colors to be used"""
        return [
            ImageColor.getcolor(color_hex, "RGB") for color_hex in list(ColorMapper.COLOR_MAP.keys())
        ]
