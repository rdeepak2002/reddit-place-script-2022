# Reddit Place Script 2022

[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

## About

This is a script to draw a image onto r/place (<https://www.reddit.com/r/place/>).

## Features

- Support for multiple accounts
- Determines the cooldown time remaining for each account
- Detects existing matching pixels on the r/place map and skips them
- Automatically converts colors to the r/place color palette

## Requirements

- [Latest Version of Python 3](https://www.python.org/downloads/)
- [A Reddit App Client ID and App Secret Key](https://www.reddit.com/prefs/apps)

## How to Get App Client ID and App Secret Key

You need to generate an app client id and app secret key for each account in order to use this script.

Steps:

1. Visit <https://www.reddit.com/prefs/apps>
2. Click "create (another) app" button at very bottom
3. Select the "script" option and fill in the fields with anything

If you don't want to create a development app for each account, you can add each username as a developer in the developer app settings. You will need to duplicate the client ID and secret in .env, though.

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

Change the values to what its supposed to be

- username Username of accounts
- passsword Passwords for account
- client_id Workers client id for the app / script registered with Reddit
- client_secret Workers secret keys for the app / script registered with Reddit
- image_start_coords Specifies the root position (x,y) to draw the image on the r/place canvas
- start_coords Specifies which x/y position of the original image to start at while drawing it

### Notes: 
- Change image.jpg to specify what image to draw. One pixel is drawn every 5 minutes

## Run the Script

```python
python3 main.py
```

## Multiple Workers

Just create multiple child arrays to "workers" in the .json

```json
{
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

```text
{
    "thread_delay": 2,
}
```

- thread_delay Adds a delay between starting a new thread. Can be used to avoid ratelimiting

- Transparency can be achieved by using the RGB value (69, 42, 0) in any part of your image
- If you'd like, you can enable Verbose Mode by adding --verbose to "python main.py". This will output a lot more information, and not neccessarily in the right order, but it is useful for development and debugging.

## Developing
The nox CI job will run flake8 on the code. You can also do this locally by pip installing nox on your system and running 
`nox` in the repository directory.
