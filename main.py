# imports
import os
import math
import requests
import json
import time
from requests.auth import HTTPBasicAuth
from dotenv import load_dotenv

# map of colors for pixels you can place
color_map = {
    "#FF4500": 2, # bright red
    "#FFA800": 3, # orange
    "#FFD635": 4, # yellow
    "#00A36": 6, # darker green
    "#7EED56": 8, # lighter green
    "#2450A4": 12, # darkest blue
    "#3690EA": 13, # medium normal blue
    "#51E9F4": 14, # cyan
    "#811E9F": 18, # darkest purple
    "#B44AC0": 19, # normal purple
    "#FF99AA": 23, # pink
    "#9C6926": 25, # brown
    "#000000": 27, # black
    "#898D90": 29, # grey
    "#D4D7D9": 30, # light grey
    "#FFFFFF": 31, # white
}

# pixel drawing preferences
pixel_x = 999
pixel_y = 997
pixel_color_index = color_map["#FFFFFF"]

# load env variables
load_dotenv()

# important variable for auth
# developer's reddit username and password
username = os.getenv('ENV_PLACE_USERNAME')
password = os.getenv('ENV_PLACE_PASSWORD')
# note: use https://www.reddit.com/prefs/apps
app_client_id = os.getenv('ENV_PLACE_APP_CLIENT_ID')
secret_key = os.getenv('ENV_PLACE_SECRET_KEY')

# global variables for script
access_token = None
current_timestamp = math.floor(time.time())
last_time_placed_pixel = math.floor(time.time())
access_token_expires_at_timestamp = math.floor(time.time())

# note: reddit limits us to place 1 pixel every 5 minutes
pixel_place_frequency = 300


def set_pixel(access_token_in, x, y, color_index_in=18, canvas_index=0):
    print("placing pixel")

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

# def run():
while True:
    current_timestamp = math.floor(time.time())

    # refresh access token if necessary
    if access_token is None or current_timestamp >= expires_at_timestamp:
        print("refreshing access token...")

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
        access_token_type = response_data["token_type"] # this is just "bearer"
        access_token_expires_in_seconds = response_data["expires_in"] # this is usually "3600"
        access_token_scope = response_data["scope"] # this is usually "*"

        # ts stores the time in seconds
        expires_at_timestamp = current_timestamp + int(access_token_expires_in_seconds)

        print("received new access token: ", access_token)

    # draw pixel onto screen
    if access_token is not None and current_timestamp >= last_time_placed_pixel + pixel_place_frequency:
        set_pixel(access_token, pixel_x, pixel_y, pixel_color_index)
        last_time_placed_pixel = math.floor(time.time())
