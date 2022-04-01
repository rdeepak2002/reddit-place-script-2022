# imports
import os
import math
import requests
import json
import time
from requests.auth import HTTPBasicAuth
from dotenv import load_dotenv
from PIL import ImageColor
from PIL import Image

# load env variables
load_dotenv()

# map of colors for pixels you can place
color_map = {
    "#FF4500": 2,  # bright red
    "#FFA800": 3,  # orange
    "#FFD635": 4,  # yellow
    "#00A368": 6,  # darker green
    "#7EED56": 8,  # lighter green
    "#2450A4": 12,  # darkest blue
    "#3690EA": 13,  # medium normal blue
    "#51E9F4": 14,  # cyan
    "#811E9F": 18,  # darkest purple
    "#B44AC0": 19,  # normal purple
    "#FF99AA": 23,  # pink
    "#9C6926": 25,  # brown
    "#000000": 27,  # black
    "#898D90": 29,  # grey
    "#D4D7D9": 30,  # light grey
    "#FFFFFF": 31,  # white
}

# color palette
rgb_colors_array = []

# auth variables
access_token = None
access_token_expires_at_timestamp = math.floor(time.time())

# image.jpg information
pix = None
image_width = None
image_height = None


# function to convert rgb tuple to hexadecimal string
def rgb_to_hex(rgb):
    return ('#%02x%02x%02x' % rgb).upper()


# function to find the closest rgb color from palette to a target rgb color
def closest_color(target_rgb, rgb_colors_array_in):
    r, g, b = target_rgb
    color_diffs = []
    for color in rgb_colors_array_in:
        cr, cg, cb = color
        color_diff = math.sqrt((r - cr) ** 2 + (g - cg) ** 2 + (b - cb) ** 2)
        color_diffs.append((color_diff, color))
    return min(color_diffs)[1]


# method to draw a pixel at an x, y coordinate in r/place with a specific color
def set_pixel(access_token_in, x, y, color_index_in=18, canvas_index=0):
    print("placing pixel with color index " + str(color_index_in) + " at " + str((x, y)))

    url = "https://gql-realtime-2.reddit.com/query"

    payload = json.dumps({
        "operationName": "setPixel",
        "variables": {
            "input": {
                "actionName": "r/replace:set_pixel",
                "PixelMessageData": {
                    "coordinate": {
                        "x": x,
                        "y": y
                    },
                    "colorIndex": color_index_in,
                    "canvasIndex": canvas_index
                }
            }
        },
        "query": "mutation setPixel($input: ActInput!) {\n  act(input: $input) {\n    data {\n      ... on BasicMessage {\n        id\n        data {\n          ... on GetUserCooldownResponseMessageData {\n            nextAvailablePixelTimestamp\n            __typename\n          }\n          ... on SetPixelResponseMessageData {\n            timestamp\n            __typename\n          }\n          __typename\n        }\n        __typename\n      }\n      __typename\n    }\n    __typename\n  }\n}\n"
    })
    headers = {
        'origin': 'https://hot-potato.reddit.com',
        'referer': 'https://hot-potato.reddit.com/',
        'apollographql-client-name': 'mona-lisa',
        'Authorization': 'Bearer ' + access_token_in,
        'Content-Type': 'application/json'
    }

    response = requests.request("POST", url, headers=headers, data=payload)

    print(response.text)


# method to define the color palette array
def init_rgb_colors_array():
    global rgb_colors_array

    # generate array of available rgb colors we can use
    for color_hex, color_index in color_map.items():
        rgb_array = ImageColor.getcolor(color_hex, "RGB")
        rgb_colors_array.append(rgb_array)

    print("available colors for palette (rgb): ", rgb_colors_array)


# method to read the input image.jpg file
def load_image():
    global pix
    global image_width
    global image_height
    # read and load the image to draw and get its dimensions
    image_path = os.path.join(os.path.abspath(os.getcwd()), 'image.jpg')
    im = Image.open(image_path)
    pix = im.load()
    print("image size: ", im.size)  # Get the width and height of the image for iterating over
    image_width, image_height = im.size


# task to draw the input image
def task():
    # whether image should keep drawing itself
    repeat_forever = True

    while True:
        try:
            # global variables for script
            last_time_placed_pixel = math.floor(time.time())

            # note: reddit limits us to place 1 pixel every 5 minutes, so I am setting it to
            # 5 minutes and 30 seconds per pixel
            pixel_place_frequency = 330

            # pixel drawing preferences
            pixel_x_start = int(os.getenv('ENV_DRAW_X_START'))
            pixel_y_start = int(os.getenv('ENV_DRAW_Y_START'))

            # current pixel row and pixel column being drawn
            current_r = int(os.getenv('ENV_R_START'))
            current_c = int(os.getenv('ENV_C_START'))

            # string for time until next pixel is drawn
            update_str = ""

            # reference to globally shared variables such as auth token and image
            global access_token
            global access_token_expires_at_timestamp

            # refresh auth tokens and / or draw a pixel
            while True:
                # get the current time
                current_timestamp = math.floor(time.time())

                # log next time until drawing
                time_until_next_draw = last_time_placed_pixel + pixel_place_frequency - current_timestamp
                new_update_str = str(time_until_next_draw) + " seconds until next pixel is drawn"
                if update_str != new_update_str:
                    update_str = new_update_str
                    print(update_str)

                # refresh access token if necessary
                if access_token is None or current_timestamp >= access_token_expires_at_timestamp:
                    print("__________________")
                    print("refreshing access token...")

                    # developer's reddit username and password
                    username = os.getenv('ENV_PLACE_USERNAME')
                    password = os.getenv('ENV_PLACE_PASSWORD')
                    # note: use https://www.reddit.com/prefs/apps
                    app_client_id = os.getenv('ENV_PLACE_APP_CLIENT_ID')
                    secret_key = os.getenv('ENV_PLACE_SECRET_KEY')

                    data = {
                        'grant_type': 'password',
                        'username': username,
                        'password': password
                    }

                    r = requests.post("https://ssl.reddit.com/api/v1/access_token",
                                      data=data,
                                      auth=HTTPBasicAuth(app_client_id, secret_key))

                    print("received response: ", r.text)

                    response_data = r.json()
                    access_token = response_data["access_token"]
                    # access_token_type = response_data["token_type"]  # this is just "bearer"
                    access_token_expires_in_seconds = response_data["expires_in"]  # this is usually "3600"
                    # access_token_scope = response_data["scope"]  # this is usually "*"

                    # ts stores the time in seconds
                    access_token_expires_at_timestamp = current_timestamp + int(access_token_expires_in_seconds)

                    print("received new access token: ", access_token)
                    print("__________________")

                # draw pixel onto screen
                if access_token is not None and current_timestamp >= last_time_placed_pixel + pixel_place_frequency:
                    # get target color
                    target_rgb = pix[current_r, current_c]

                    # get converted color
                    new_rgb = closest_color(target_rgb, rgb_colors_array)
                    new_rgb_hex = rgb_to_hex(new_rgb)
                    pixel_color_index = color_map[new_rgb_hex]

                    # draw the pixel onto r/place
                    set_pixel(access_token, pixel_x_start + current_r, pixel_y_start + current_c, pixel_color_index)
                    last_time_placed_pixel = math.floor(time.time())

                    current_r += 1
                    current_c += 1

                    # go back to first column when reached end of a row while drawing
                    if current_r >= image_width:
                        current_r = 0

                    # exit when all pixels drawn
                    if current_c >= image_height:
                        print("__________________")
                        print("done drawing image to r/place")
                        print("__________________")
                        break
        except:
            print("__________________")
            print("Error refreshing tokens or drawing pixel")
            print("Trying again in 30 seconds...")
            print("__________________")
            time.sleep(30)

        if not repeat_forever:
            break


# get color palette
init_rgb_colors_array()

# load the pixels for the input image
load_image()

# run the image drawing task
task()
