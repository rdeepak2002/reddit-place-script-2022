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
- SOCKS proxy support
- No client id and secret needed

## Requirements

- [Latest Version of Python 3](https://www.python.org/downloads/)

## MacOSX
If you are using MacOSX and encounter an SSL_CERTIFICATE error. Please apply the fix detailed https://stackoverflow.com/questions/42098126/mac-osx-python-ssl-sslerror-ssl-certificate-verify-failed-certificate-verify  


## Get Started

Move the file 'config_example.json' to config.json

Edit the values to replace with actual credentials and values

Note: Please use https://jsonlint.com/ to check that your JSON file is correctly formatted

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
      // which pixel of the image to draw first
      "start_coords": [0, 0]
    },
    // username of account 2
    "worker1username": {
      // password of account 2
      "password": "password",
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

### You can get more logs (`DEBUG`) by running the script with `-d` flag

`python3 main.py -d` or `python3 main.py --debug`

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
      "start_coords": [0, 0]
    },
    "worker2username": {
      "password": "password",
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
    "proxies": ["1.1.1.1:8080","2.2.2.2:1234"],
    "compact_logging": true
}
```

- thread_delay - Adds a delay between starting a new thread. Can be used to avoid ratelimiting
- unverified_place_frequency - Sets the pixel place frequency to the unverified account limit
- proxies - Sets proxies to use for sending requests to reddit. The proxy used is randomly selected for each request. Can be used to avoid ratelimiting
- compact_logging - Disables timer text until next pixel

- Transparency can be achieved by using the RGB value (69, 42, 0) in any part of your image
- If you'd like, you can enable Verbose Mode by adding --verbose to "python main.py". This will output a lot more information, and not neccessarily in the right order, but it is useful for development and debugging.

## Docker

A dockerfile is provided. Instructions on installing docker are outside the scope of this guide.

To build: After editing your config.json, run `docker build . -t place-bot`. and wait for the image to build

You can now run with 

`docker run place-bot`


## Contributing

See the [Contributing Guide](docs/CONTRIBUTING.md)
