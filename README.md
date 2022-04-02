# Reddit Place Script 2022

[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![forthebadge](https://forthebadge.com/images/badges/made-with-python.svg)](https://forthebadge.com)
[![forthebadge](https://forthebadge.com/images/badges/60-percent-of-the-time-works-every-time.svg)](https://forthebadge.com)

## About

This is a script to draw an image onto r/place (<https://www.reddit.com/r/place/>).

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


## MacOSX
If you are using MacOSX and encounter an SSL_CERTIFICATE error. Please apply the fix detailed https://stackoverflow.com/questions/42098126/mac-osx-python-ssl-sslerror-ssl-certificate-verify-failed-certificate-verify  


## Get Started

Move the file 'config_example.json' to config.json

Edit the values to replace with actual credentials and values

```json
{
  //Where the image's path is
  "image_path":"image.png",
  // [x,y] where you want the top left pixel of the local image to be drawn on canvas
  "image_start_coords": [741, 610],
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

- Change image.jpg/png to specify what image to draw. One pixel is drawn every 5 minutes. PNG takes priority over JPG.

## Run the Script

### Windows

```shell
start.bat or startverbose.bat
```

### Other OS

```shell
chmod +x start.sh startverbose.sh
./start.sh or ./startverbose.sh
```

## Multiple Workers

Just create multiple child arrays to "workers" in the .json

```json
{
  "image_path":"image.png",
  "image_start_coords": [741, 610],
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

If any JSON decoders errors are found, the `config.json` needs a fix. Make sure to add the below 2 lines in the file.

```text
{
    "thread_delay": 2,
    "unverified_place_frequency": false,
}
```

- thread_delay - Adds a delay between starting a new thread. Can be used to avoid ratelimiting
- unverified_place_frequency - Sets the pixel place frequency to the unverified account limit

- Transparency can be achieved by using the RGB value (69, 42, 0) in any part of your image
- If you'd like, you can enable Verbose Mode by adding --verbose to "python main.py". This will output a lot more information, and not neccessarily in the right order, but it is useful for development and debugging.

## Docker

A dockerfile is provided. Instructions on installing docker are outside the scope of this guide.

To build: After editing your config.json, run `docker build . -t place-bot`. and wait for the image to build

You can now run with 

`docker run place-bot`


## Developing

The nox CI job will run flake8 and black on the code. You can also do this locally by pip installing nox on your system and running `nox` in the repository directory.
