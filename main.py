import os
import os.path
import math
import requests
import json
import time
import threading
from io import BytesIO
from websocket import create_connection
from requests.auth import HTTPBasicAuth
from dotenv import load_dotenv
from PIL import ImageColor
from PIL import Image
import random
import json

# Todo: use logging

# set verbose mode to increase output (messy)
verbose_mode = False

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

# map of pixel color ids to verbose name (for debugging)
name_map = {
    2: "Bright Red",
    3: "Orange",
    4: "Yellow",
    6: "Dark Green",
    8: "Light Green",
    12: "Dark Blue",
    13: "Blue",
    14: "Cyan",
    18: "Dark Purple",
    19: "Purple",
    23: "Pink",
    25: "Brown",
    27: "Black",
    29: "Grey",
    30: "Light Grey",
    31: "White",
}


class PlaceClient:
    def __init__(self):
        # Data
        self.json_data = self.get_json_data()
        self.pixel_x_start: int = self.json_data["image_start_coords"][0]
        self.pixel_y_start: int = self.json_data["image_start_coords"][1]

        # In seconds
        self.delay_between_launches = self.json_data[
            "thread_delay"] if self.json_data["thread_delay"] != None else 3
        
        # Color palette
        self.rgb_colors_array = self.generate_rgb_colors_array()

        # Auth
        self.access_tokens = {}
        self.access_token_expires_at_timestamp = {}

        # Image information
        self.pix = None
        self.image_size = None

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

    def closest_color(self, target_rgb):
        r, g, b = target_rgb
        color_diffs = []
        for color in self.rgb_colors_array:
            cr, cg, cb = color
            color_diff = math.sqrt(
                (r - cr) ** 2 + (g - cg) ** 2 + (b - cb) ** 2)
            color_diffs.append((color_diff, color))
        return min(color_diffs)[1]

    # Define the color palette array
    def generate_rgb_colors_array(self):
        # Generate array of available rgb colors to be used
        return [ImageColor.getcolor(color_hex, "RGB") for color_hex, _i in color_map.items()]

    def get_json_data(self):
        if not os.path.exists("config.json"):
            exit("No config.json file found. Read the README")

        # To not keep file open whole execution time
        f = open("config.json")
        json_data = json.load(f)
        f.close()

        return json_data

    # Read the input image.jpg file

    def load_image(self):
        # Read and load the image to draw and get its dimensions
        im = Image.open(os.path.join(
            os.path.abspath(os.getcwd()), "image.jpg"))
        self.pix = im.load()
        print(
            "Image size: ", im.size
        )
        self.image_size = im.size

    """ Main """
    # Draw a pixel at an x, y coordinate in r/place with a specific color
    def set_pixel_and_check_ratelimit(
        self,
        access_token_in, x, y, color_index_in=18, canvas_index=0
    ):
        print("Placing " + self.color_id_to_name(color_index_in) +
              " pixel at " + str((x, y)))

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
        if verbose_mode:
            print("received response: ", response.text)
        # There are 2 different JSON keys for responses to get the next timestamp.
        # If we don't get data, it means we've been rate limited.
        # If we do, a pixel has been successfully placed.
        if response.json()["data"] == None:
            waitTime = math.floor(
                response.json()[
                    "errors"][0]["extensions"]["nextAvailablePixelTs"]
            )
            print("placing failed: rate limited")
        else:
            waitTime = math.floor(
                response.json()["data"]["act"]["data"][0]["data"][
                    "nextAvailablePixelTimestamp"
                ]
            )
            print("placing succeeded")

        # THIS COMMENTED CODE LETS YOU DEBUG THREADS FOR TESTING
        # Works perfect with one thread.
        # With multiple threads, every time you press Enter you move to the next one.
        # Move the code anywhere you want, I put it here to inspect the API responses.

        # import code

        # code.interact(local=locals())

        # Reddit returns time in ms and we need seconds, so divide by 1000
        return waitTime / 1000

    def get_board(self, access_token_in):
        print("Getting board")
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
        print("Got image:", file)

        return boardimg

    def get_unset_pixel(self, boardimg, x, y):
        pix2 = Image.open(boardimg).convert("RGB").load()
        num_loops = 0
        while True:
            x += 1

            if x >= self.image_size[0]:
                y += 1
                x = 0

            if y >= self.image_size[1]:
                if num_loops > 1:
                    target_rgb = self.pix[self.pixel_x_start,
                                          self.pixel_y_start]
                    new_rgb = self.closest_color(target_rgb)
                    return self.pixel_x_start, self.pixel_y_start, new_rgb
                y = self.pixel_y_start
                num_loops += 1
            if verbose_mode:
                print(x + self.pixel_x_start, y + self.pixel_y_start)
                print(x, y, "boardimg", self.image_size[0], self.image_size[1])
            target_rgb = self.pix[x, y]
            new_rgb = self.closest_color(target_rgb)
            if pix2[x + self.pixel_x_start, y + self.pixel_y_start] != new_rgb:
                if verbose_mode:
                    print(
                        pix2[x + self.pixel_x_start, y + self.pixel_y_start],
                        new_rgb,
                        new_rgb != (69, 42, 0),
                        pix2[x, y] != new_rgb,
                    )
                if new_rgb != (69, 42, 0):
                    if verbose_mode:
                        print(
                            "Different Pixel found at:",
                            x + self.pixel_x_start,
                            y + self.pixel_y_start,
                            "With Color:",
                            pix2[x + self.pixel_x_start,
                                 y + self.pixel_y_start],
                            "Replacing with:",
                            new_rgb,
                        )
                    break
                else:
                    print("TransparrentPixel")
        return x, y, new_rgb

    # Draw the input image
    def task(self, index, name, worker):
        # Whether image should keep drawing itself
        repeat_forever = True

        while True:
            last_time_placed_pixel = math.floor(time.time())

            # note: Reddit limits us to place 1 pixel every 5 minutes, so I am setting it to
            # 5 minutes and 30 seconds per pixel
            pixel_place_frequency = 330

            try:
                # Current pixel row and pixel column being drawn
                current_x = worker["start_coords"][0]
                current_y = worker["start_coords"][1]
            except Exception:
                print(
                    f"You need to provide start_coords to worker '{name}'",
                )
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
                time_until_next_draw = (
                    last_time_placed_pixel + pixel_place_frequency - current_timestamp
                )

                new_update_str = f"{time_until_next_draw} seconds until next pixel is drawn"
                if update_str != new_update_str and time_until_next_draw % 10 == 0:
                    update_str = new_update_str
                    print(
                        "-------Thread #"
                        + str(index)
                        + "-------\n"
                        + update_str
                    )

                # refresh access token if necessary
                if (
                    len(self.access_tokens) == 0 or
                    len(self.access_token_expires_at_timestamp) == 0 or
                    index in self.access_tokens
                    or current_timestamp
                    >= self.access_token_expires_at_timestamp[index]
                ):
                    print(
                        "-------Thread #"
                        + str(index)
                        + "-------\n"
                        + "Refreshing access token..."
                    )

                    # developer's reddit username and password
                    try:
                        username = name
                        password = worker["password"]
                        # note: use https://www.reddit.com/prefs/apps
                        app_client_id = worker["client_id"]
                        secret_key = worker["client_secret"]
                    except Exception:
                        print(
                            f"You need to provide all required fields to worker '{name}'",
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
                        headers={
                            "User-agent": f"placebot{random.randint(1, 100000)}"},
                    )

                    if verbose_mode:
                        print("Received response: ", r.text)

                    response_data = r.json()

                    if "error" in response_data:
                        print(f"An error occured. Make sure you have the correct credentials. Response data: {response_data}")
                        exit(1)

                    self.access_tokens[index] = response_data["access_token"]
                    # access_token_type = response_data["token_type"]  # this is just "bearer"
                    access_token_expires_in_seconds = response_data[
                        "expires_in"
                    ]  # this is usually "3600"
                    # access_token_scope = response_data["scope"]  # this is usually "*"

                    # ts stores the time in seconds
                    self.access_token_expires_at_timestamp[
                        index
                    ] = current_timestamp + int(access_token_expires_in_seconds)

                    print(
                        "Received new access token: ",
                        self.access_tokens[index],
                    )

                # draw pixel onto screen
                if self.access_tokens[index] is not None and (
                    current_timestamp >= last_time_placed_pixel + pixel_place_frequency
                    or self.first_run_counter <= index
                ):

                    # place pixel immediately
                    # first_run = False
                    self.first_run_counter += 1

                    # get target color
                    # target_rgb = pix[current_r, current_c]

                    # get current pixel position from input image and replacement color
                    current_x, current_y, new_rgb = self.get_unset_pixel(
                        self.get_board(self.access_tokens[index]),
                        current_x,
                        current_y,
                    )

                    # get converted color
                    new_rgb_hex = self.rgb_to_hex(new_rgb)
                    pixel_color_index = color_map[new_rgb_hex]

                    # draw the pixel onto r/place
                    last_time_placed_pixel = self.set_pixel_and_check_ratelimit(
                        self.access_tokens[index],
                        self.pixel_x_start + current_x,
                        self.pixel_y_start + current_y,
                        pixel_color_index,
                    )

                    current_x += 1

                    # go back to first column when reached end of a row while drawing
                    if current_x >= self.image_size[0]:
                        current_x = 0
                        current_y += 1

                    # exit when all pixels drawn
                    if current_y >= self.image_size[1]:
                        print(
                            "--------Thread #"
                            + str(index)
                            + "--------\n"
                            + "done drawing image to r/place\n"
                        )
                        break

            if not repeat_forever:
                break

    def start(self):
        for index, worker in enumerate(self.json_data["workers"]):
            threading.Thread(target=self.task, args=[
                             index, worker, self.json_data["workers"][worker]]).start()
            # exit(1)
            time.sleep(self.delay_between_launches)


if __name__ == "__main__":
    client = PlaceClient()
    # Start everything
    client.start()
