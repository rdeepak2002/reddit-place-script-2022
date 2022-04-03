#!/usr/bin/env python3

import os
import os.path
import math
import requests
import json
import logging
import time
import threading
import sys
import random
from io import BytesIO
from websocket import create_connection
from PIL import ImageColor
from PIL import Image, UnidentifiedImageError
from loguru import logger
import click
from bs4 import BeautifulSoup


from mappings import color_map, name_map


class PlaceClient:
    def __init__(self, config_path):
        # Data
        self.json_data = self.get_json_data(config_path)
        self.pixel_x_start: int = self.json_data["image_start_coords"][0]
        self.pixel_y_start: int = self.json_data["image_start_coords"][1]

        # In seconds
        self.delay_between_launches = (
            self.json_data["thread_delay"]
            if "thread_delay" in self.json_data and
            self.json_data["thread_delay"] is not None
            else 3
        )
        self.unverified_place_frequency = (
            self.json_data["unverified_place_frequency"]
            if "unverified_place_frequency" in self.json_data and
            self.json_data["unverified_place_frequency"] is not None
            else False
        )
        self.proxies = (
            self.GetProxies(self.json_data["proxies"])
            if "proxies" in self.json_data and
            self.json_data["proxies"] is not None
            else None
        )
        self.compactlogging = (
            self.json_data["compact_logging"]
            if "compact_logging" in self.json_data and
            self.json_data["compact_logging"] is not None
            else True
        )

        # Color palette
        self.rgb_colors_array = self.generate_rgb_colors_array()

        # Auth
        self.access_tokens = {}
        self.access_token_expires_at_timestamp = {}

        # Image information
        self.pix = None
        self.image_size = None
        self.image_path = (
            self.json_data["image_path"]
            if "image_path" in self.json_data
            else "image.jpg"
        )
        self.first_run_counter = 0

        # Initialize-functions
        self.load_image()

    """ Utils """
    # Convert rgb tuple to hexadecimal string

    def rgb_to_hex(self, rgb):
        return ("#%02x%02x%02x" % rgb).upper()

    # More verbose color indicator from a pixel color ID
    def color_id_to_name(self, color_id):
        if color_id in name_map.keys():
            return "{} ({})".format(name_map[color_id], str(color_id))
        return "Invalid Color ({})".format(str(color_id))

    # Find the closest rgb color from palette to a target rgb color

    def GetProxies(self, proxies):
        proxieslist = []
        for i in proxies:
            proxieslist.append({"https": i})
        return proxieslist

    def GetRandomProxy(self):
        randomproxy = None
        if self.proxies is not None:
            randomproxy = self.proxies[random.randint(0, len(self.proxies) - 1)]
        return randomproxy

    def closest_color(self, target_rgb):
        r, g, b = target_rgb
        color_diffs = []
        for color in self.rgb_colors_array:
            cr, cg, cb = color
            color_diff = math.sqrt((r - cr) ** 2 + (g - cg) ** 2 + (b - cb) ** 2)
            color_diffs.append((color_diff, color))
        return min(color_diffs)[1]

    # Define the color palette array
    def generate_rgb_colors_array(self):
        # Generate array of available rgb colors to be used
        return [
            ImageColor.getcolor(color_hex, "RGB") for color_hex, _i in color_map.items()
        ]

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
            logger.fatal("Failed to load image")
            exit()
        except UnidentifiedImageError:
            logger.fatal("File found, but couldn't identify image format")
        self.pix = im.load()
        logger.info("Loaded image size: {}", im.size)
        self.image_size = im.size

    """ Main """
    # Draw a pixel at an x, y coordinate in r/place with a specific color

    def set_pixel_and_check_ratelimit(
        self, access_token_in, x, y, color_index_in=18, canvas_index=0, thread_index=-1
    ):
        logger.info(
            "Thread #{} : Attempting to place {} pixel at {}, {}",
            thread_index,
            self.color_id_to_name(color_index_in),
            x + (1000 * canvas_index),
            y,
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

        response = requests.request(
            "POST", url, headers=headers, data=payload, proxies=self.GetRandomProxy()
        )
        logger.debug("Thread #{} : Received response: {}", thread_index, response.text)

        # There are 2 different JSON keys for responses to get the next timestamp.
        # If we don't get data, it means we've been rate limited.
        # If we do, a pixel has been successfully placed.
        if response.json()["data"] is None:
            waitTime = math.floor(
                response.json()["errors"][0]["extensions"]["nextAvailablePixelTs"]
            )
            logger.error("Thread #{} : Failed placing pixel: rate limited", thread_index)
        else:
            waitTime = math.floor(
                response.json()["data"]["act"]["data"][0]["data"][
                    "nextAvailablePixelTimestamp"
                ]
            )
            logger.info("Thread #{} : Succeeded placing pixel", thread_index)

        # THIS COMMENTED CODE LETS YOU DEBUG THREADS FOR TESTING
        # Works perfect with one thread.
        # With multiple threads, every time you press Enter you move to the next one.
        # Move the code anywhere you want, I put it here to inspect the API responses.

        # Reddit returns time in ms and we need seconds, so divide by 1000
        return waitTime / 1000

    def get_board(self, access_token_in):
        logger.debug("Connecting and obtaining board images")
        ws = create_connection(
            "wss://gql-realtime-2.reddit.com/query",
            origin="https://hot-potato.reddit.com",
        )
        ws.send(
            json.dumps(
                {
                    "type": "connection_init",
                    "payload": {"Authorization": "Bearer " + access_token_in},
                }
            )
        )
        while True:
            msg = ws.recv()
            if msg is None:
                logger.error("Reddit failed to acknowledge connection_init")
                exit()
            if msg.startswith('{"type":"connection_ack"}'):
                logger.debug("Connected to WebSocket server")
                break
        logger.debug("Obtaining Canvas information")
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

        while True:
            canvas_payload = json.loads(ws.recv())
            if canvas_payload["type"] == "data":
                canvas_details = canvas_payload["payload"]["data"]["subscribe"]["data"]
                logger.debug("Canvas config: {}", canvas_payload)
                break

        canvas_sockets = []

        canvas_count = len(canvas_details["canvasConfigurations"])

        for i in range(0, canvas_count):
            canvas_sockets.append(2 + i)
            logger.debug("Creating canvas socket {}", canvas_sockets[i])

            ws.send(
                json.dumps(
                    {
                        "id": str(2 + i),
                        "type": "start",
                        "payload": {
                            "variables": {
                                "input": {
                                    "channel": {
                                        "teamOwner": "AFD2022",
                                        "category": "CANVAS",
                                        "tag": str(i),
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

        imgs = []
        logger.debug("A total of {} canvas sockets opened", len(canvas_sockets))
        while len(canvas_sockets) > 0:
            temp = json.loads(ws.recv())
            logger.debug("Waiting for WebSocket message")
            if temp["type"] == "data":
                logger.debug("Received WebSocket data type message")
                msg = temp["payload"]["data"]["subscribe"]
                if msg["data"]["__typename"] == "FullFrameMessageData":
                    logger.debug("Received full frame message")
                    img_id = int(temp["id"])
                    logger.debug("Image ID: {}", img_id)
                    if img_id in canvas_sockets:
                        logger.debug("Getting image: {}", msg["data"]["name"])
                        imgs.append(
                            Image.open(
                                BytesIO(
                                    requests.get(
                                        msg["data"]["name"], stream=True
                                    ).content
                                )
                            )
                        )
                        canvas_sockets.remove(img_id)
                        logger.debug(
                            "Canvas sockets remaining: {}", len(canvas_sockets)
                        )

        for i in range(0, canvas_count - 1):
            ws.send(json.dumps({"id": str(2 + i), "type": "stop"}))

        ws.close()

        # TODO: Multiply by canvas_details["canvasConfigurations"][i]["dx"] and canvas_details["canvasConfigurations"][i]["dy"] instead of hardcoding it
        new_img_width = int(canvas_details["canvasWidth"]) * 2
        logger.debug("New image width: {}", new_img_width)
        new_img_height = int(canvas_details["canvasHeight"])
        logger.debug("New image height: {}", new_img_height)

        new_img = Image.new("RGB", (new_img_width, new_img_height))
        dx_offset = 0
        for idx, img in enumerate(imgs):
            logger.debug("Adding image: {}", img)
            dx_offset = int(canvas_details["canvasConfigurations"][idx]["dx"])
            new_img.paste(img, (dx_offset, 0))

        return new_img

    def get_unset_pixel(self, boardimg, x, y, index):
        pix2 = boardimg.convert("RGB").load()
        while True:
            if x >= self.image_size[0]:
                y += 1
                x = 0

            if y >= self.image_size[1]:
                logging.info("Thread #{} : All pixels correct, trying again in 10 seconds... ", index)

                time.sleep(10)

                boardimg = self.get_board(self.access_tokens[index])
                pix2 = boardimg.convert("RGB").load()
                y = 0

            logger.debug("{}, {}", x + self.pixel_x_start, y + self.pixel_y_start)
            logger.debug(
                "{}, {}, boardimg, {}, {}", x, y, self.image_size[0], self.image_size[1]
            )

            target_rgb = self.pix[x, y][:3]

            new_rgb = self.closest_color(target_rgb)
            if pix2[x + self.pixel_x_start, y + self.pixel_y_start] != new_rgb:
                logger.debug(
                    "{}, {}, {}, {}",
                    pix2[x + self.pixel_x_start, y + self.pixel_y_start],
                    new_rgb,
                    target_rgb != (69, 42, 0),
                    pix2[x, y] != new_rgb,
                )
                if target_rgb != (69, 42, 0):
                    logger.debug(
                        "Thread #{} : Replacing {} pixel at: {},{} with {} color",
                        index,
                        pix2[x + self.pixel_x_start, y + self.pixel_y_start],
                        x + self.pixel_x_start,
                        y + self.pixel_y_start,
                        new_rgb,
                    )
                    break
                else:
                    logger.info("TransparrentPixel")
            x += 1
        return x, y, new_rgb

    # Draw the input image
    def task(self, index, name, worker):
        # Whether image should keep drawing itself
        repeat_forever = True

        while True:
            # last_time_placed_pixel = math.floor(time.time())

            # note: Reddit limits us to place 1 pixel every 5 minutes, so I am setting it to
            # 5 minutes and 30 seconds per pixel
            if self.unverified_place_frequency:
                pixel_place_frequency = 1230
            else:
                pixel_place_frequency = 330

            next_pixel_placement_time = math.floor(time.time()) + pixel_place_frequency

            try:
                # Current pixel row and pixel column being drawn
                current_r = worker["start_coords"][0]
                current_c = worker["start_coords"][1]
            except Exception:
                logger.info("You need to provide start_coords to worker '{}'", name)
                exit(1)

            # Time until next pixel is drawn
            update_str = ""

            # Refresh auth tokens and / or draw a pixel
            while True:
                # reduce CPU usage
                time.sleep(1)

                # get the current time
                current_timestamp = math.floor(time.time())

                # log next time until drawing
                time_until_next_draw = next_pixel_placement_time - current_timestamp

                if time_until_next_draw > 10000:
                    logger.info(f"Thread #{index} :: CANCELLED :: Rate-Limit Banned")
                    exit(1)

                new_update_str = (
                    f"{time_until_next_draw} seconds until next pixel is drawn"
                )

                if update_str != new_update_str and time_until_next_draw % 10 == 0:
                    update_str = new_update_str
                else:
                    update_str = ""

                if len(update_str) > 0:
                    if not self.compactlogging:
                        logger.info("Thread #{} :: {}", index, update_str)

                # refresh access token if necessary
                if (
                    len(self.access_tokens) == 0 or
                    len(self.access_token_expires_at_timestamp) == 0 or
                    # index in self.access_tokens
                    index not in self.access_token_expires_at_timestamp or
                    (
                        self.access_token_expires_at_timestamp.get(index) and
                        current_timestamp >=
                        self.access_token_expires_at_timestamp.get(index)
                    )
                ):
                    if not self.compactlogging:
                        logger.info("Thread #{} :: Refreshing access token", index)

                    # developer's reddit username and password
                    try:
                        username = name
                        password = worker["password"]
                        # note: use https://www.reddit.com/prefs/apps
                    except Exception:
                        logger.info(
                            "You need to provide all required fields to worker '{}'",
                            name,
                        )
                        exit(1)

                    client = requests.Session()
                    r = client.get("https://www.reddit.com/login")
                    login_get_soup = BeautifulSoup(r.content, "html.parser")
                    csrf_token = login_get_soup.find("input", {"name": "csrf_token"})[
                        "value"
                    ]
                    data = {
                        "username": username,
                        "password": password,
                        "dest": "https://www.reddit.com/",
                        "csrf_token": csrf_token,
                    }

                    r = client.post(
                        "https://www.reddit.com/login",
                        data=data,
                        proxies=self.GetRandomProxy(),
                    )
                    if r.status_code != 200:
                        print("Authorization failed!")  # password is probably invalid
                        return
                    else:
                        print("Authorization successful!")
                    print("Obtaining access token...")
                    r = client.get("https://www.reddit.com/")
                    data_str = (
                        BeautifulSoup(r.content, features="html.parser")
                        .find("script", {"id": "data"})
                        .contents[0][len("window.__r = "): -1]
                    )
                    data = json.loads(data_str)
                    response_data = data["user"]["session"]

                    if "error" in response_data:
                        logger.info(
                            "An error occured. Make sure you have the correct credentials. Response data: {}",
                            response_data,
                        )
                        exit(1)

                    self.access_tokens[index] = response_data["accessToken"]
                    # access_token_type = data["user"]["session"]["accessToken"]  # this is just "bearer"
                    access_token_expires_in_seconds = response_data[
                        "expiresIn"
                    ]  # this is usually "3600"
                    # access_token_scope = response_data["scope"]  # this is usually "*"

                    # ts stores the time in seconds
                    self.access_token_expires_at_timestamp[
                        index
                    ] = current_timestamp + int(access_token_expires_in_seconds)
                    if not self.compactlogging:
                        logger.info(
                            "Received new access token: {}************",
                            self.access_tokens.get(index)[:5],
                        )

                # draw pixel onto screen
                if self.access_tokens.get(index) is not None and (
                    current_timestamp >= next_pixel_placement_time or
                    self.first_run_counter <= index
                ):

                    # place pixel immediately
                    # first_run = False
                    self.first_run_counter += 1

                    # get target color
                    # target_rgb = pix[current_r, current_c]

                    # get current pixel position from input image and replacement color
                    current_r, current_c, new_rgb = self.get_unset_pixel(
                        self.get_board(self.access_tokens[index]),
                        current_r,
                        current_c,
                        index,
                    )

                    # get converted color
                    new_rgb_hex = self.rgb_to_hex(new_rgb)
                    pixel_color_index = color_map[new_rgb_hex]

                    logger.info("\nAccount Placing: ", name, "\n")

                    # draw the pixel onto r/place
                    # There's a better way to do this
                    canvas = 0
                    pixel_x_start = self.pixel_x_start + current_r
                    pixel_y_start = self.pixel_y_start + current_c
                    while pixel_x_start > 999:
                        pixel_x_start -= 1000
                        canvas += 1

                    # draw the pixel onto r/place
                    next_pixel_placement_time = self.set_pixel_and_check_ratelimit(
                        self.access_tokens[index],
                        pixel_x_start,
                        pixel_y_start,
                        pixel_color_index,
                        canvas,
                        index
                    )

                    current_r += 1

                    # go back to first column when reached end of a row while drawing
                    if current_r >= self.image_size[0]:
                        current_r = 0
                        current_c += 1

                    # exit when all pixels drawn
                    if current_c >= self.image_size[1]:
                        logger.info("Thread #{} :: image completed", index)
                        break

            if not repeat_forever:
                break

    def start(self):
        for index, worker in enumerate(self.json_data["workers"]):
            threading.Thread(
                target=self.task,
                args=[index, worker, self.json_data["workers"][worker]],
            ).start()
            # exit(1)
            time.sleep(self.delay_between_launches)


@click.command()
@click.option(
    "-d",
    "--debug",
    is_flag=True,
    help="Enable debug mode. Prints debug messages to the console.",
)
@click.option(
    "-c",
    "--config",
    default="config.json",
    help="Location of config.json",
)
def main(debug: bool, config: str):

    if not debug:
        # default loguru level is DEBUG
        logger.remove()
        logger.add(sys.stderr, level="INFO")

    client = PlaceClient(config_path=config)
    # Start everything
    client.start()


if __name__ == "__main__":
    main()
