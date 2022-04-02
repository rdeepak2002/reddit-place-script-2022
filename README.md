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
ENV_PLACE_USERNAME='["developer_username"]'
ENV_PLACE_PASSWORD='["developer_password"]'
ENV_PLACE_APP_CLIENT_ID='["app_client_id"]'
ENV_PLACE_SECRET_KEY='["app_secret_key"]'
ENV_DRAW_X_START="x_position_start_integer"
ENV_DRAW_Y_START="y_position_start_integer"
ENV_R_START='["0"]'
ENV_C_START='["0"]'
```

- ENV_PLACE_USERNAME is the username of the developer account
- ENV_PLACE_PASSWORD is the password of the developer account
- ENV_PLACE_APP_CLIENT_ID is the client id for the app / script registered with Reddit
- ENV_PLACE_SECRET_KEY is the secret key for the app / script registered with Reddit
- ENV_DRAW_X_START specifies the x position to draw the image on the r/place canvas
- ENV_DRAW_Y_START specifies the y position to draw the image on the r/place canvas
- ENV_R_START specifies which x position of the original image to start at while drawing it
- ENV_C_START specifies which y position of the original image to start at while drawing it


Note: Multiple fields can be passed into the arrays to spawn a thread for each one.

Change image.jpg to specify what image to draw. One pixel is drawn every 5 minutes and only jpeg images are supported.

## Run the Script

```
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

The same pattern can be used for 3 or more threads drawing at once. Note that the "ENV_PLACE_USERNAME", "ENV_PLACE_PASSWORD", "ENV_PLACE_APP_CLIENT_ID", "ENV_PLACE_SECRET_KEY", "ENV_R_START", and "ENV_C_START" variables should all be string arrays of the same size.

Also note that I did the following in the above example:

```text
ENV_R_START='["0", "0"]'
ENV_C_START='["0", "50"]'
```

In this case, the first worker will start drawing from (0, 0) and the second worker will start drawing from (0, 50) from the input image.jpg file. 

This is useful if you want different threads drawing different parts of the image with different accounts. 
