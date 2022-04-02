# Reddit Place Script 2022

[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

## About

This is a script to draw a JPG onto r/place (<https://www.reddit.com/r/place/>).

## Features

- Support for multiple accounts
- Determines the cooldown time remaining for each account
- Detects existing matching pixels on the r/place map and skips them
- Automatically converts colors to the r/place color palette

## Requirements

- [Python 3](https://www.python.org/downloads/)
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

```shell
pip3 install -r requirements.txt
```

## Get Started

Create a file called '.env'

Put in the following content:

```text
ENV_PLACE_USERNAME='["developer_username"]'
ENV_PLACE_PASSWORD='["developer_password"]'
ENV_PLACE_APP_CLIENT_ID='["app_client_id"]'
ENV_PLACE_SECRET_KEY='["app_secret_key"]'
ENV_DRAW_X_START="x_position_start_integer"
ENV_DRAW_Y_START="y_position_start_integer"
ENV_R_START='["0"]'
ENV_C_START='["0"]'
```

- ENV_PLACE_USERNAME is an array of usernames of developer accounts
- ENV_PLACE_PASSWORD is an array of the passwords of developer accounts
- ENV_PLACE_APP_CLIENT_ID is an array of the client ids for the app / script registered with Reddit
- ENV_PLACE_SECRET_KEY is an array of the secret keys for the app / script registered with Reddit
- ENV_DRAW_X_START specifies the x position to draw the image on the r/place canvas
- ENV_DRAW_Y_START specifies the y position to draw the image on the r/place canvas
- ENV_R_START is an array which specifies which x position of the original image to start at while drawing it
- ENV_C_START is an array which specifies which y position of the original image to start at while drawing it

Note: Multiple fields can be passed into the arrays to spawn a thread for each one.

Change image.jpg to specify what image to draw. One pixel is drawn every 5 minutes and only jpeg images are supported.

## Run the Script

```python
python3 main.py
```

## Multiple Workers

If you want two threads drawing the image at once you could have a setup like this:

```text
ENV_PLACE_USERNAME='["developer_username_1", "developer_username_2"]'
ENV_PLACE_PASSWORD='["developer_password_1", "developer_password_2"]'
ENV_PLACE_APP_CLIENT_ID='["app_client_id_1", "app_client_id_2"]'
ENV_PLACE_SECRET_KEY='["app_secret_key_1", "app_secret_key_2"]'
ENV_DRAW_X_START="x_position_start_integer"
ENV_DRAW_Y_START="y_position_start_integer"
ENV_R_START='["0", "0"]'
ENV_C_START='["0", "50"]'
```

The same pattern can be used for multiple drawing at once. Note that the "ENV_PLACE_USERNAME", "ENV_PLACE_PASSWORD", "ENV_PLACE_APP_CLIENT_ID", "ENV_PLACE_SECRET_KEY", "ENV_R_START", and "ENV_C_START" variables MUST be string arrays of the same size.

Also note that I did the following in the above example:

```text
ENV_R_START='["0", "0"]'
ENV_C_START='["0", "50"]'
```

In this case, the first worker will start drawing from (0, 0) and the second worker will start drawing from (0, 50) from the input image.jpg file.

This is useful if you want different threads drawing different parts of the image with different accounts.

If you'd like, you can enable Verbose Mode by editing the Python file. This will output a lot more information, and not neccessarily in the right order, but it is useful for development and debugging.

## Other Settings

```text
ENV_THREAD_DELAY='0'
ENV_UNVERIFIED_PLACE_FREQUENCY='True'
```

- ENV_THREAD_DELAY Adds a delay between starting a new thread. Can be used to avoid ratelimiting
- ENV_UNVERIFIED_PLACE_FREQUENCY is for setting the pixel place frequency to the unverified account frequency (20 minutes)


## Developing
The nox CI job will run flake8 on the code. You can also do this locally by pip installing nox on your system and running 
`nox` in the repository directory.