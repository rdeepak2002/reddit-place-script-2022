# Place CMU on Reddit r/place

We want to put our cmu banner on r/place (https://www.reddit.com/r/place/) right under `Pitt` at around (683, 507)

## How to contribute

### Step 1: Get App Client ID and App Secret Key

You need to generate an app client id and app secret key in order to use this script.

Steps:

1. Visit https://www.reddit.com/prefs/apps
2. Click `create (another) app` button at very bottom 
3. Select the `script` option and fill in the fields with anything
4. "redirection": you can fill it as `https://www.reddit.com/r/place/`. It doesn't matter


### Step 2: Download Code
1. download the code by `git clone git@github.com:KokeCacao/reddit-place-script-2022.git`
2. Create a file called `.env` right besides `README.md`, this is your setting file
3. Put in the following content:

```text
ENV_PLACE_USERNAME='["your_reddit_developer_username"]'
ENV_PLACE_PASSWORD='["your_reddit_password"]'
ENV_PLACE_APP_CLIENT_ID='["app_client_id"]'
ENV_PLACE_SECRET_KEY='["app_secret_key"]'
ENV_DRAW_X_START="666"
ENV_DRAW_Y_START="513"
ENV_R_START='["0"]'
ENV_C_START='["0"]'
```

- ENV_PLACE_USERNAME is the username of the developer account
- ENV_PLACE_PASSWORD is the password of the developer account
- ENV_PLACE_APP_CLIENT_ID is the client id for the app / script registered with Reddit (under "personal use script", something like `Q98s00Gkb7CnOZgXoj917Q`)
- ENV_PLACE_SECRET_KEY is the secret key for the app / script registered with Reddit (above "name", something like `LKfIHcTs5pct0VZPgXT99IgAUXpTsg`)
- ENV_DRAW_X_START don't change it
- ENV_DRAW_Y_START don't change it
- ENV_R_START don't change it
- ENV_C_START don't change it


### Step 3 - Option 1: Using Conda (recommended)
Install [Python 3](https://www.python.org/downloads/) if you haven't

```shell
conda create --name reddit python=3.8
conda activate reddit
conda install --yes --file requirements.txt
conda install --yes pillow requests python-dotenv
python3 main.py
```

### Step 3 - Option 2: Using Pip
Install [Python 3](https://www.python.org/downloads/) if you haven't

```shell
pip3 install -r requirements.txt
python3 main.py
```

Note: Multiple fields can be passed into the arrays to spawn a thread for each one.
