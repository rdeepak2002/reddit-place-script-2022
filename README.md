# Reddit Place Script 2022

[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![forthebadge](https://forthebadge.com/images/badges/made-with-python.svg)](https://forthebadge.com)
[![forthebadge](https://forthebadge.com/images/badges/60-percent-of-the-time-works-every-time.svg)](https://forthebadge.com)

## About

This is a script to draw the offical TUX onto r/place (<https://www.reddit.com/r/place/>).

## Features

- Support for multiple accounts
- Determines the cooldown time remaining for each account
- Detects existing matching pixels on the r/place map and skips them
- Automatically converts colors to the r/place color palette
- Easy(ish) to read output with colors

## Requirements

- [Latest Version of Python 3](https://www.python.org/downloads/)
- [A Reddit App Client ID and App Secret Key](https://www.reddit.com/prefs/apps)

## How to Get App Client ID and App Secret Key

You need to generate an app client id and app secret key for each account in order to use this script. Or, just create one, and add each username as a developer in the developer app settings. You will need to duplicate the client ID and secret in .env, though.

Steps:

1. Visit <https://www.reddit.com/prefs/apps>
2. Click "create (another) app" button at very bottom
3. Select the "script" option and fill in the fields with anything

<img width="383" alt="App ID Screenshot" src="https://user-images.githubusercontent.com/19873803/161398668-0705f122-51d3-4785-8bd9-d6700b586634.png">

## Python Package Requirements

Install requirements from 'requirements.txt' file.

### Windows

```shell
pip install -r requirements.txt
```

### Other OS

```shell
pip3 install -r requirements.txt
```

## Get Started

Move the file 'config_example.json' to config.json

Edit the values to replace with actual credentials and values

```json
{
  //Where the image's path is
  "image_path":"image.png",
  // [x,y] where you want the top left pixel of the local image to be drawn on canvas
  "image_start_coords": [20, 679],
  // delay between starting threads (can be 0)
  "thread_delay": 2,
  // array of accounts to use
  "workers": {
    // username of account 1
    "worker1username": {
      // password of account 1
      "password": "password",
      // appid and secret (see How To Get App Client ID And App Secret Key)
      "client_id": "clientid",
      "client_secret": "clientsecret",
      // which pixel of the image to draw first
      "start_coords": [0, 0]
    },
    // username of account 2
    "worker1username": {
      // password of account 2
      "password": "password",
      // appid and secret (see How To Get App Client ID And App Secret Key)
      "client_id": "clientid",
      "client_secret": "clientsecret",
      // which pixel of the image to draw first
      "start_coords": [0, 0]
    }
    // etc... add as many accounts as you want (but reddit may detect you the more you add)
  }
}
```

### Notes

Note: Multiple fields can be passed into the arrays to spawn a thread for each one.

## Run the Script

```python
python3 main.py
```

## Multiple Workers

Just create multiple child arrays to "workers" in the .json

```json
{
  "image_start_coords": [20, 679],
  "thread_delay": 2,

  "workers": {
    "worker1username": {
      "password": "password",
      "client_id": "clientid",
      "client_secret": "clientsecret",
      "start_coords": [0, 0]
    },
    "worker2username": {
      "password": "password",
      "client_id": "clientid",
      "client_secret": "clientsecret",
      "start_coords": [0, 50]
    }
  }
}
```

In this case, the first worker will start drawing from (0, 0) and the second worker will start drawing from (0, 50) from the input image.jpg file.

This is useful if you want different threads drawing different parts of the image with different accounts.

## Other Settings

```text
{
    "thread_delay": 2,
    "unverified_place_frequency": False,
}
```

- thread_delay - Adds a delay between starting a new thread. Can be used to avoid ratelimiting
- unverified_place_frequency - Sets the pixel place frequency to the unverified account limit

## Developing
The nox CI job will run flake8 on the code. You can also do this locally by pip installing nox on your system and running 
`nox` in the repository directory.
