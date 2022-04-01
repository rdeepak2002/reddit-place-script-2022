# Reddit Place Script 2022

## About

Script to draw pixels onto r/place (https://www.reddit.com/r/place/)

## Requirements

- Python 3 (https://www.python.org/downloads/)

## How to Get App Client ID and App Secret Key

- Visit https://www.reddit.com/prefs/apps
- Click "create (another) app" button at very bottom
- Select the "script" option and fill in the fields with anything

## Get Started

Create a file called '.env'

Put in the following content:

```text
ENV_PLACE_USERNAME="developer_username"
ENV_PLACE_PASSWORD="developer_password"
ENV_PLACE_APP_CLIENT_ID="app_client_id"
ENV_PLACE_SECRET_KEY="app_secret_key"
```

Edit the variables at the top to specify what pixel to draw and where to draw it.

## Python Package Requirements

Install requirements from 'requirements.txt' file.

```shell
pip3 install -r requirements.txt
```