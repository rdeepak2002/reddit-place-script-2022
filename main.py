import os
import os.path
import math
import requests
import json
import time
import threading
import logging
import colorama
import argparse
import sys
from io import BytesIO
from websocket import create_connection
from requests.auth import HTTPBasicAuth
from dotenv import load_dotenv
from PIL import ImageColor
from PIL import Image
import random


from mappings import color_map, name_map

# Option remains for legacy usage
# equal to running
# python main.py --verbose
verbose_mode = False


# function to convert rgb tuple to hexadecimal string
def rgb_to_hex(rgb):
    return ("#%02x%02x%02x" % rgb).upper()


# Get a more verbose color indicator from a pixel color ID
def color_id_to_name(color_id):
    if color_id in name_map.keys():
        return "{} ({})".format(name_map[color_id], str(color_id))
    return "Invalid Color ({})".format(str(color_id))


# function to find the closest rgb color from palette to a target rgb color
def closest_color(target_rgb, rgb_colors_array_in):
    r, g, b = target_rgb[:3] # trim rgba tuple to rgb if png
    
    color_diffs = []
    for color in rgb_colors_array_in:
        cr, cg, cb = color
        color_diff = math.sqrt((r - cr) ** 2 + (g - cg) ** 2 + (b - cb) ** 2)
        color_diffs.append((color_diff, color))
    return min(color_diffs)[1]


# method to draw a pixel at an x, y coordinate in r/place with a specific color
def set_pixel_and_check_ratelimit(
    access_token_in, x, y, color_index_in=18, canvas_index=0
):
    logging.info(
        f"Attempting to place {color_id_to_name(color_index_in)} pixel at {x}, {y}"
    )

    url = "https://gql-realtime-2.reddit.com/query"

    payload = json.dumps(
        {
            "operationName": "setPixel",
            "variables": {
                "input": {
                    "actionName": "r/replace:set_pixel",
                    "PixelMessageData": {
                        "coordinate": {"x": x, "y": y},
                        "colorIndex": color_index_in,
                        "canvasIndex": canvas_index,
                    },
                }
            },
            "query": "mutation setPixel($input: ActInput!) {\n  act(input: $input) {\n    data {\n      ... on BasicMessage {\n        id\n        data {\n          ... on GetUserCooldownResponseMessageData {\n            nextAvailablePixelTimestamp\n            __typename\n          }\n          ... on SetPixelResponseMessageData {\n            timestamp\n            __typename\n          }\n          __typename\n        }\n        __typename\n      }\n      __typename\n    }\n    __typename\n  }\n}\n",
        }
    )
    headers = {
        "origin": "https://hot-potato.reddit.com",
        "referer": "https://hot-potato.reddit.com/",
        "apollographql-client-name": "mona-lisa",
        "Authorization": "Bearer " + access_token_in,
        "Content-Type": "application/json",
    }

    response = requests.request("POST", url, headers=headers, data=payload)
    logging.debug(f"Received response: {response.text}")
    # There are 2 different JSON keys for responses to get the next timestamp.
    # If we don't get data, it means we've been rate limited.
    # If we do, a pixel has been successfully placed.
    if response.json()["data"] is None:
        waitTime = math.floor(
            response.json()["errors"][0]["extensions"]["nextAvailablePixelTs"]
        )
        logging.info(
            f"{colorama.Fore.RED}Failed placing pixel: rate limited {colorama.Style.RESET_ALL}"
        )
    else:
        waitTime = math.floor(
            response.json()["data"]["act"]["data"][0]["data"][
                "nextAvailablePixelTimestamp"
            ]
        )
        logging.info(
            f"{colorama.Fore.GREEN}Succeeded placing pixel {colorama.Style.RESET_ALL}"
        )

    # THIS COMMENTED CODE LETS YOU DEBUG THREADS FOR TESTING
    # Works perfect with one thread.
    # With multiple threads, every time you press Enter you move to the next one.
    # Move the code anywhere you want, I put it here to inspect the API responses.

    # import code

    # code.interact(local=locals())

    # Reddit returns time in ms and we need seconds, so divide by 1000
    return waitTime / 1000


def get_board(access_token_in):
    logging.info("Getting board")
    ws = create_connection(
        "wss://gql-realtime-2.reddit.com/query", origin="https://hot-potato.reddit.com"
    )
    ws.send(
        json.dumps(
            {
                "type": "connection_init",
                "payload": {"Authorization": "Bearer " + access_token_in},
            }
        )
    )
    ws.recv()
    ws.send(
        json.dumps(
            {
                "id": "1",
                "type": "start",
                "payload": {
                    "variables": {
                        "input": {
                            "channel": {
                                "teamOwner": "AFD2022",
                                "category": "CONFIG",
                            }
                        }
                    },
                    "extensions": {},
                    "operationName": "configuration",
                    "query": "subscription configuration($input: SubscribeInput!) {\n  subscribe(input: $input) {\n    id\n    ... on BasicMessage {\n      data {\n        __typename\n        ... on ConfigurationMessageData {\n          colorPalette {\n            colors {\n              hex\n              index\n              __typename\n            }\n            __typename\n          }\n          canvasConfigurations {\n            index\n            dx\n            dy\n            __typename\n          }\n          canvasWidth\n          canvasHeight\n          __typename\n        }\n      }\n      __typename\n    }\n    __typename\n  }\n}\n",
                },
            }
        )
    )
    ws.recv()
    ws.send(
        json.dumps(
            {
                "id": "2",
                "type": "start",
                "payload": {
                    "variables": {
                        "input": {
                            "channel": {
                                "teamOwner": "AFD2022",
                                "category": "CANVAS",
                                "tag": "0",
                            }
                        }
                    },
                    "extensions": {},
                    "operationName": "replace",
                    "query": "subscription replace($input: SubscribeInput!) {\n  subscribe(input: $input) {\n    id\n    ... on BasicMessage {\n      data {\n        __typename\n        ... on FullFrameMessageData {\n          __typename\n          name\n          timestamp\n        }\n        ... on DiffFrameMessageData {\n          __typename\n          name\n          currentTimestamp\n          previousTimestamp\n        }\n      }\n      __typename\n    }\n    __typename\n  }\n}\n",
                },
            }
        )
    )

    file = ""
    while True:
        temp = json.loads(ws.recv())
        if temp["type"] == "data":
            msg = temp["payload"]["data"]["subscribe"]
            if msg["data"]["__typename"] == "FullFrameMessageData":
                file = msg["data"]["name"]
                break

    ws.close()

    boardimg = BytesIO(requests.get(file, stream=True).content)
    logging.info(f"Received board image: {file}")

    return boardimg


def get_unset_pixel(boardimg, x, y):
    pixel_x_start = int(os.getenv("ENV_DRAW_X_START"))
    pixel_y_start = int(os.getenv("ENV_DRAW_Y_START"))
    pix2 = Image.open(boardimg).convert("RGB").load()
    num_loops = 0
    while True:
        x += 1

        if x >= image_width:
            y += 1
            x = 0

        if y >= image_height:
            if num_loops > 1:
                target_rgb = pix[0, 0]
                new_rgb = closest_color(target_rgb, rgb_colors_array)
                return 0, 0, new_rgb
            y = 0
            num_loops += 1
        logging.debug(f"{x+pixel_x_start}, {y+pixel_y_start}")
        logging.debug(f"{x}, {y}, boardimg, {image_width}, {image_height}")

        target_rgb = pix[x, y]
        new_rgb = closest_color(target_rgb, rgb_colors_array)
        if pix2[x + pixel_x_start, y + pixel_y_start] != new_rgb:
            logging.debug(
                f"{pix2[x + pixel_x_start, y + pixel_y_start]}, {new_rgb}, {new_rgb != (69, 42, 0)}, {pix2[x, y] != new_rgb,}"
            )
            if new_rgb != (69, 42, 0):
                logging.debug(
                    f"Replacing {pix2[x+pixel_x_start, y+pixel_y_start]} pixel at: {x+pixel_x_start},{y+pixel_y_start} with {new_rgb} color"
                )
                break
            else:
                print("TransparrentPixel")
    return x, y, new_rgb


# method to define the color palette array
def init_rgb_colors_array():
    global rgb_colors_array

    # generate array of available rgb colors we can use
    for color_hex, color_index in color_map.items():
        rgb_array = ImageColor.getcolor(color_hex, "RGB")
        rgb_colors_array.append(rgb_array)
    logging.debug(f"Available colors for rgb palette: {rgb_colors_array}")


# method to read the input image.jpg file
def load_image():
    global pix
    global image_width
    global image_height
    global image_extension

    # read and load the image to draw and get its dimensions
    valid_image_extensions = [".png", ".jpg", ".jpeg"] # List your valid image extensions here

    image_path = None
    for extension in valid_image_extensions:
        path = os.path.join(os.path.abspath(os.getcwd()), "image" + extension)
        if os.path.exists(path):
            image_path = path
            image_extension = extension
            break
    
    if image_path is None:
        sys.exit("No valid image path found!")
    
    print('Loading image from ' + image_path)
    im = Image.open(image_path)
    pix = im.load()
    logging.info(f"Loaded image size: {im.size}")
    image_width, image_height = im.size


# task to draw the input image
def task(credentials_index):
    # whether image should keep drawing itself
    repeat_forever = True

    while True:
        # try:
        # global variables for script
        last_time_placed_pixel = math.floor(time.time())

        # note: reddit limits us to place 1 pixel every 5 minutes, so I am setting it to
        # 5 minutes and 30 seconds per pixel
        # pixel_place_frequency = 330
        if os.getenv("ENV_UNVERIFIED_PLACE_FREQUENCY") is not None:
            if bool(os.getenv("ENV_UNVERIFIED_PLACE_FREQUENCY")):
                pixel_place_frequency = 1230
            else:
                pixel_place_frequency = 330
        else:
            pixel_place_frequency = 330

        # pixel drawing preferences
        pixel_x_start = int(os.getenv("ENV_DRAW_X_START"))
        pixel_y_start = int(os.getenv("ENV_DRAW_Y_START"))

        try:
            # current pixel row and pixel column being drawn
            current_r = int(json.loads(os.getenv("ENV_R_START"))[credentials_index])
            current_c = int(json.loads(os.getenv("ENV_C_START"))[credentials_index])
        except IndexError:
            print(
                "Array length error: are you sure you have an ENV_R_START and ENV_C_START item for every account?\n",
                "Example for 5 accounts:\n",
                'ENV_R_START=\'["0","5","6","7","9"]\'\n',
                'ENV_C_START=\'["0","5","6","8","9"]\'\n',
                "Note: There can be duplicate entries, but every array must have the same amount of items.",
            )
            exit(1)

        # string for time until next pixel is drawn
        update_str = ""

        # reference to globally shared variables such as auth token and image
        global access_tokens
        global access_token_expires_at_timestamp

        # boolean to place a pixel the moment the script is first run
        # global first_run
        global first_run_counter

        # refresh auth tokens and / or draw a pixel
        while True:
            # reduce CPU usage
            time.sleep(1)

            # get the current time
            current_timestamp = math.floor(time.time())

            # log next time until drawing
            time_until_next_draw = (
                last_time_placed_pixel + pixel_place_frequency - current_timestamp
            )
            new_update_str = (
                str(time_until_next_draw) + " seconds until next pixel is drawn"
            )
            if update_str != new_update_str and time_until_next_draw % 10 == 0:
                update_str = new_update_str
                logging.info(f"Thread #{credentials_index} :: {update_str}")

            # refresh access token if necessary
            if (
                access_tokens[credentials_index] is None
                or current_timestamp
                >= access_token_expires_at_timestamp[credentials_index]
            ):
                logging.info(f"Thread #{credentials_index} :: Refreshing access token")

                # developer's reddit username and password
                try:
                    username = json.loads(os.getenv("ENV_PLACE_USERNAME"))[
                        credentials_index
                    ]
                    password = json.loads(os.getenv("ENV_PLACE_PASSWORD"))[
                        credentials_index
                    ]
                    # note: use https://www.reddit.com/prefs/apps
                    app_client_id = json.loads(os.getenv("ENV_PLACE_APP_CLIENT_ID"))[
                        credentials_index
                    ]
                    secret_key = json.loads(os.getenv("ENV_PLACE_SECRET_KEY"))[
                        credentials_index
                    ]
                except IndexError:
                    print(
                        "Array length error: are you sure your credentials have an equal amount of items?\n",
                        "Example for 2 accounts:\n",
                        'ENV_PLACE_USERNAME=\'["Username1", "Username2]\'\n',
                        'ENV_PLACE_PASSWORD=\'["Password", "Password"]\'\n',
                        'ENV_PLACE_APP_CLIENT_ID=\'["NBVSIBOPVAINCVIAVBOVV", "VNOPSNSJVQNVNJVSNVDV"]\'\n',
                        'ENV_PLACE_SECRET_KEY=\'["INSVDSINDJV_SVTNNJSNVNJV", "ANIJCINLLPJCSCOJNCA_ASDV"]\'\n',
                        "Note: There can be duplicate entries, but every array must have the same amount of items.",
                    )
                    exit(1)

                data = {
                    "grant_type": "password",
                    "username": username,
                    "password": password,
                }

                r = requests.post(
                    "https://ssl.reddit.com/api/v1/access_token",
                    data=data,
                    auth=HTTPBasicAuth(app_client_id, secret_key),
                    headers={"User-agent": f"placebot{random.randint(1, 100000)}"},
                )

                logging.debug(f"Received response: {r.text}")
                response_data = r.json()
                access_tokens[credentials_index] = response_data["access_token"]
                # access_token_type = response_data["token_type"]  # this is just "bearer"
                access_token_expires_in_seconds = response_data[
                    "expires_in"
                ]  # this is usually "3600"
                # access_token_scope = response_data["scope"]  # this is usually "*"

                # ts stores the time in seconds
                access_token_expires_at_timestamp[
                    credentials_index
                ] = current_timestamp + int(access_token_expires_in_seconds)
                logging.info(
                    f"Received new access token: {access_tokens[credentials_index][:5]}************"
                )

            # draw pixel onto screen
            if access_tokens[credentials_index] is not None and (
                current_timestamp >= last_time_placed_pixel + pixel_place_frequency
                or first_run_counter <= credentials_index
            ):

                # place pixel immediately
                # first_run = False
                first_run_counter += 1

                # get target color
                # target_rgb = pix[current_r, current_c]

                # get current pixel position from input image and replacement color
                current_r, current_c, new_rgb = get_unset_pixel(
                    get_board(access_tokens[credentials_index]),
                    current_r,
                    current_c,
                )

                # get converted color
                new_rgb_hex = rgb_to_hex(new_rgb)
                pixel_color_index = color_map[new_rgb_hex]

                # draw the pixel onto r/place
                last_time_placed_pixel = set_pixel_and_check_ratelimit(
                    access_tokens[credentials_index],
                    pixel_x_start + current_r,
                    pixel_y_start + current_c,
                    pixel_color_index,
                )

                current_r += 1

                # go back to first column when reached end of a row while drawing
                if current_r >= image_width:
                    current_r = 0
                    current_c += 1

                # exit when all pixels drawn
                if current_c >= image_height:
                    logging.info(f"Thread #{credentials_index} :: image completed")
                    break
        # except:
        #     print("__________________")
        #     print("Thread #" + str(credentials_index))
        #     print("Error refreshing tokens or drawing pixel")
        #     print("Trying again in 5 minutes...")
        #     print("__________________")
        #     time.sleep(5 * 60)

        if not repeat_forever:
            break


# # # # #  MAIN # # # # # #


if __name__ == "__main__":

    parser = argparse.ArgumentParser()
    colorama.init()
    parser.add_argument(
        "-v",
        "--verbose",
        help="Be verbose",
        action="store_const",
        dest="loglevel",
        const=logging.DEBUG,
        default=logging.INFO,
    )
    args = parser.parse_args()

    logging.basicConfig(
        level=(logging.DEBUG if verbose_mode else args.loglevel),
        format="[%(asctime)s] :: [%(levelname)s] - %(message)s",
        datefmt="%d-%b-%y %H:%M:%S",
    )
    logging.info("place-script started")
    if os.path.exists("./.env"):
        # load env variables
        load_dotenv()
    else:
        envfile = open(".env", "w")
        envfile.write(
            """ENV_PLACE_USERNAME='["developer_username"]'
ENV_PLACE_PASSWORD='["developer_password"]'
ENV_PLACE_APP_CLIENT_ID='["app_client_id"]'
ENV_PLACE_SECRET_KEY='["app_secret_key"]'
ENV_DRAW_X_START="x_position_start_integer"
ENV_DRAW_Y_START="y_position_start_integer"
ENV_R_START='["0"]'
ENV_C_START='["0"]\'"""
        )
        print(
            "No .env file found. A template has been created for you.",
            "Read the README and configure it properly.",
            "Right now, it's full of example data, so you ABSOLUTELY MUST edit it.",
        )
        logging.fatal("No .env file found")
        exit()

    # color palette
    rgb_colors_array = []

    # auth variables
    access_tokens = []
    access_token_expires_at_timestamp = []

    # image.jpg information
    pix = None
    image_width = None
    image_height = None

    # place a pixel immediately
    # first_run = True
    first_run_counter = 0

    # get color palette
    init_rgb_colors_array()

    # load the pixels for the input image
    load_image()

    # get number of concurrent threads to start
    num_credentials = len(json.loads(os.getenv("ENV_PLACE_USERNAME")))

    # define delay between starting new threads
    if os.getenv("ENV_THREAD_DELAY") is not None:
        delay_between_launches_seconds = int(os.getenv("ENV_THREAD_DELAY"))
    else:
        delay_between_launches_seconds = 3

    # launch a thread for each account specified in .env
    for i in range(num_credentials):
        # run the image drawing task
        access_tokens.append(None)
        access_token_expires_at_timestamp.append(math.floor(time.time()))
        thread1 = threading.Thread(target=task, args=[i])
        thread1.start()
        time.sleep(delay_between_launches_seconds)
