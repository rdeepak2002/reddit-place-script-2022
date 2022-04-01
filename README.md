# Reddit Place Script 2022

## About

Script to draw an image onto r/place (https://www.reddit.com/r/place/)

## Requirements

Python 3 (https://www.python.org/downloads/)

## How to Get App Client ID and App Secret Key

You need to generate an app client id and app secret key in order to use this script.

Steps:

1. Visit https://www.reddit.com/prefs/apps
2. Click "create (another) app" button at very bottom 
3. Select the "script" option and fill in the fields with anything

## Python Package Requirements

Install requirements from 'requirements.txt' file.

```shell
pip3 install -r requirements.txt
```

## Get Started

Create a file called '.env'

Put in the following content:

```text
ENV_PLACE_USERNAME="developer_username"
ENV_PLACE_PASSWORD="developer_password"
ENV_PLACE_APP_CLIENT_ID="app_client_id"
ENV_PLACE_SECRET_KEY="app_secret_key"
ENV_DRAW_X_START="x_position_start_integer"
ENV_DRAW_Y_START="y_position_start_integer"
```

Change image.jpg to specify what image to draw. Note: one pixel is drawn every 5 minutes and only jpeg images are supported.

## Run the Script

```
python3 main.py
```
