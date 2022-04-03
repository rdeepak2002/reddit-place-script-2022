import json
import os
from PIL import Image, UnidentifiedImageError


def get_json_data(self, config_path):
    configFilePath = os.path.join(os.getcwd(), config_path)

    if not os.path.exists(configFilePath):
        exit("No config.json file found. Read the README")

    # To not keep file open whole execution time
    f = open(configFilePath)
    json_data = json.load(f)
    f.close()

    return json_data

    # Read the input image.jpg file


def load_image(self):
    # Read and load the image to draw and get its dimensions
    try:
        im = Image.open(self.image_path)
    except FileNotFoundError:
        self.logger.exception("Failed to load image")
        exit()
    except UnidentifiedImageError:
        self.logger.exception("File found, but couldn't identify image format")

    # Convert all images to RGBA - Transparency should only be supported with PNG
    if im.mode != "RGBA":
        im = im.convert("RGBA")
        self.logger.info("Converted to rgba")
    self.pix = im.load()

    self.logger.info("Loaded image size: {}", im.size)

    self.image_size = im.size
