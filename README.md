# Reddit Place Script 2022

[![Code style: black](data:image/svg+xml;base64,PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHdpZHRoPSIyMDMuMjciIGhlaWdodD0iMzUiIHZpZXdCb3g9IjAgMCAyMDMuMjcgMzUiPjxyZWN0IGNsYXNzPSJzdmdfX3JlY3QiIHg9IjAiIHk9IjAiIHdpZHRoPSIxMjIuMSIgaGVpZ2h0PSIzNSIgZmlsbD0iIzY0NjQ2NCIvPjxyZWN0IGNsYXNzPSJzdmdfX3JlY3QiIHg9IjEyMC4xIiB5PSIwIiB3aWR0aD0iODMuMTcwMDAwMDAwMDAwMDIiIGhlaWdodD0iMzUiIGZpbGw9IiMwMDAwMDAiLz48cGF0aCBjbGFzcz0ic3ZnX190ZXh0IiBkPSJNMTMuOTUgMTguMTlMMTMuOTUgMTguMTlMMTMuOTUgMTcuMzlRMTMuOTUgMTYuMTkgMTQuMzggMTUuMjdRMTQuODAgMTQuMzUgMTUuNjAgMTMuODVRMTYuNDAgMTMuMzUgMTcuNDUgMTMuMzVMMTcuNDUgMTMuMzVRMTguODYgMTMuMzUgMTkuNzMgMTQuMTJRMjAuNTkgMTQuODkgMjAuNzMgMTYuMjlMMjAuNzMgMTYuMjlMMTkuMjUgMTYuMjlRMTkuMTQgMTUuMzcgMTguNzEgMTQuOTZRMTguMjggMTQuNTUgMTcuNDUgMTQuNTVMMTcuNDUgMTQuNTVRMTYuNDggMTQuNTUgMTUuOTcgMTUuMjZRMTUuNDUgMTUuOTYgMTUuNDQgMTcuMzNMMTUuNDQgMTcuMzNMMTUuNDQgMTguMDlRMTUuNDQgMTkuNDcgMTUuOTMgMjAuMjBRMTYuNDMgMjAuOTIgMTcuMzggMjAuOTJMMTcuMzggMjAuOTJRMTguMjUgMjAuOTIgMTguNjkgMjAuNTNRMTkuMTMgMjAuMTQgMTkuMjUgMTkuMjJMMTkuMjUgMTkuMjJMMjAuNzMgMTkuMjJRMjAuNjAgMjAuNTkgMTkuNzIgMjEuMzVRMTguODQgMjIuMTIgMTcuMzggMjIuMTJMMTcuMzggMjIuMTJRMTYuMzYgMjIuMTIgMTUuNTkgMjEuNjNRMTQuODEgMjEuMTUgMTQuMzkgMjAuMjZRMTMuOTcgMTkuMzcgMTMuOTUgMTguMTlaTTI0Ljc3IDE4LjAwTDI0Ljc3IDE4LjAwTDI0Ljc3IDE3LjUyUTI0Ljc3IDE2LjI4IDI1LjIxIDE1LjMyUTI1LjY1IDE0LjM3IDI2LjQ2IDEzLjg2UTI3LjI3IDEzLjM1IDI4LjMxIDEzLjM1UTI5LjM1IDEzLjM1IDMwLjE2IDEzLjg1UTMwLjk2IDE0LjM1IDMxLjQwIDE1LjI5UTMxLjg0IDE2LjIzIDMxLjg1IDE3LjQ4TDMxLjg1IDE3LjQ4TDMxLjg1IDE3Ljk2UTMxLjg1IDE5LjIxIDMxLjQxIDIwLjE2UTMwLjk4IDIxLjEwIDMwLjE4IDIxLjYxUTI5LjM3IDIyLjEyIDI4LjMyIDIyLjEyTDI4LjMyIDIyLjEyUTI3LjI4IDIyLjEyIDI2LjQ3IDIxLjYxUTI1LjY2IDIxLjEwIDI1LjIyIDIwLjE3UTI0Ljc4IDE5LjIzIDI0Ljc3IDE4LjAwWk0yNi4yNSAxNy40NkwyNi4yNSAxNy45NlEyNi4yNSAxOS4zNiAyNi44MCAyMC4xM1EyNy4zNSAyMC45MCAyOC4zMiAyMC45MEwyOC4zMiAyMC45MFEyOS4zMSAyMC45MCAyOS44NCAyMC4xNVEzMC4zNyAxOS40MCAzMC4zNyAxNy45NkwzMC4zNyAxNy45NkwzMC4zNyAxNy41MVEzMC4zNyAxNi4wOSAyOS44MyAxNS4zNFEyOS4yOSAxNC41OCAyOC4zMSAxNC41OEwyOC4zMSAxNC41OFEyNy4zNSAxNC41OCAyNi44MSAxNS4zM1EyNi4yNiAxNi4wOSAyNi4yNSAxNy40NkwyNi4yNSAxNy40NlpNMzguNzcgMjJMMzYuMzEgMjJMMzYuMzEgMTMuNDdMMzguODMgMTMuNDdRMzkuOTYgMTMuNDcgNDAuODQgMTMuOTdRNDEuNzIgMTQuNDggNDIuMjAgMTUuNDBRNDIuNjggMTYuMzMgNDIuNjggMTcuNTJMNDIuNjggMTcuNTJMNDIuNjggMTcuOTVRNDIuNjggMTkuMTYgNDIuMTkgMjAuMDhRNDEuNzEgMjEuMDAgNDAuODIgMjEuNTBRMzkuOTIgMjIgMzguNzcgMjJMMzguNzcgMjJaTTM3LjgwIDE0LjY2TDM3LjgwIDIwLjgyTDM4Ljc2IDIwLjgyUTM5LjkzIDIwLjgyIDQwLjU1IDIwLjA5UTQxLjE4IDE5LjM2IDQxLjE5IDE3Ljk5TDQxLjE5IDE3Ljk5TDQxLjE5IDE3LjUyUTQxLjE5IDE2LjEzIDQwLjU4IDE1LjQwUTM5Ljk4IDE0LjY2IDM4LjgzIDE0LjY2TDM4LjgzIDE0LjY2TDM3LjgwIDE0LjY2Wk01Mi43MiAyMkw0Ny4xNCAyMkw0Ny4xNCAxMy40N0w1Mi42OCAxMy40N0w1Mi42OCAxNC42Nkw0OC42MiAxNC42Nkw0OC42MiAxNy4wMkw1Mi4xMyAxNy4wMkw1Mi4xMyAxOC4xOUw0OC42MiAxOC4xOUw0OC42MiAyMC44Mkw1Mi43MiAyMC44Mkw1Mi43MiAyMlpNNjIuNDYgMTkuNDJMNjIuNDYgMTkuNDJMNjMuOTQgMTkuNDJRNjMuOTQgMjAuMTUgNjQuNDIgMjAuNTVRNjQuOTAgMjAuOTUgNjUuODAgMjAuOTVMNjUuODAgMjAuOTVRNjYuNTcgMjAuOTUgNjYuOTYgMjAuNjNRNjcuMzUgMjAuMzIgNjcuMzUgMTkuODBMNjcuMzUgMTkuODBRNjcuMzUgMTkuMjQgNjYuOTUgMTguOTRRNjYuNTYgMTguNjMgNjUuNTMgMTguMzJRNjQuNTAgMTguMDEgNjMuODkgMTcuNjNMNjMuODkgMTcuNjNRNjIuNzIgMTYuOTAgNjIuNzIgMTUuNzJMNjIuNzIgMTUuNzJRNjIuNzIgMTQuNjkgNjMuNTYgMTQuMDJRNjQuNDAgMTMuMzUgNjUuNzQgMTMuMzVMNjUuNzQgMTMuMzVRNjYuNjQgMTMuMzUgNjcuMzMgMTMuNjhRNjguMDMgMTQuMDEgNjguNDMgMTQuNjFRNjguODMgMTUuMjIgNjguODMgMTUuOTZMNjguODMgMTUuOTZMNjcuMzUgMTUuOTZRNjcuMzUgMTUuMjkgNjYuOTMgMTQuOTFRNjYuNTEgMTQuNTQgNjUuNzMgMTQuNTRMNjUuNzMgMTQuNTRRNjUuMDEgMTQuNTQgNjQuNjAgMTQuODVRNjQuMjAgMTUuMTYgNjQuMjAgMTUuNzFMNjQuMjAgMTUuNzFRNjQuMjAgMTYuMTggNjQuNjQgMTYuNTBRNjUuMDcgMTYuODEgNjYuMDcgMTcuMTBRNjcuMDYgMTcuNDAgNjcuNjcgMTcuNzhRNjguMjcgMTguMTYgNjguNTUgMTguNjVRNjguODMgMTkuMTMgNjguODMgMTkuNzlMNjguODMgMTkuNzlRNjguODMgMjAuODYgNjguMDIgMjEuNDlRNjcuMjAgMjIuMTIgNjUuODAgMjIuMTJMNjUuODAgMjIuMTJRNjQuODcgMjIuMTIgNjQuMTAgMjEuNzdRNjMuMzIgMjEuNDMgNjIuODkgMjAuODNRNjIuNDYgMjAuMjIgNjIuNDYgMTkuNDJaTTc0LjgwIDE0LjY2TDcyLjE3IDE0LjY2TDcyLjE3IDEzLjQ3TDc4LjkzIDEzLjQ3TDc4LjkzIDE0LjY2TDc2LjI3IDE0LjY2TDc2LjI3IDIyTDc0LjgwIDIyTDc0LjgwIDE0LjY2Wk04NC43MyAxOC44Nkw4MS44NiAxMy40N0w4My41MSAxMy40N0w4NS40NyAxNy41MUw4Ny40NCAxMy40N0w4OS4wOCAxMy40N0w4Ni4yMiAxOC44Nkw4Ni4yMiAyMkw4NC43MyAyMkw4NC43MyAxOC44NlpNOTguMzUgMjJMOTIuOTkgMjJMOTIuOTkgMTMuNDdMOTQuNDcgMTMuNDdMOTQuNDcgMjAuODJMOTguMzUgMjAuODJMOTguMzUgMjJaTTEwOC4wNSAyMkwxMDIuNDcgMjJMMTAyLjQ3IDEzLjQ3TDEwOC4wMSAxMy40N0wxMDguMDEgMTQuNjZMMTAzLjk1IDE0LjY2TDEwMy45NSAxNy4wMkwxMDcuNDYgMTcuMDJMMTA3LjQ2IDE4LjE5TDEwMy45NSAxOC4xOUwxMDMuOTUgMjAuODJMMTA4LjA1IDIwLjgyTDEwOC4wNSAyMloiIGZpbGw9IiNGRkZGRkYiLz48cGF0aCBjbGFzcz0ic3ZnX190ZXh0IiBkPSJNMTM4LjgzIDIyTDEzNC4yOSAyMkwxMzQuMjkgMTMuNjBMMTM4LjU5IDEzLjYwUTE0MC4xOSAxMy42MCAxNDEuMDMgMTQuMTlRMTQxLjg4IDE0Ljc5IDE0MS44OCAxNS43OUwxNDEuODggMTUuNzlRMTQxLjg4IDE2LjM5IDE0MS41OCAxNi44N1ExNDEuMjggMTcuMzQgMTQwLjc0IDE3LjYyTDE0MC43NCAxNy42MlExNDEuNDcgMTcuODcgMTQxLjg3IDE4LjQxUTE0Mi4yOCAxOC45NCAxNDIuMjggMTkuNzBMMTQyLjI4IDE5LjcwUTE0Mi4yOCAyMC44MCAxNDEuMzkgMjEuNDBRMTQwLjUwIDIyIDEzOC44MyAyMkwxMzguODMgMjJaTTEzNi42NCAxOC41OEwxMzYuNjQgMjAuMjhMMTM4LjY0IDIwLjI4UTEzOS44OCAyMC4yOCAxMzkuODggMTkuNDNMMTM5Ljg4IDE5LjQzUTEzOS44OCAxOC41OCAxMzguNjQgMTguNThMMTM4LjY0IDE4LjU4TDEzNi42NCAxOC41OFpNMTM2LjY0IDE1LjMxTDEzNi42NCAxNi45NEwxMzguMjcgMTYuOTRRMTM5LjQ3IDE2Ljk0IDEzOS40NyAxNi4xMkwxMzkuNDcgMTYuMTJRMTM5LjQ3IDE1LjMxIDEzOC4yNyAxNS4zMUwxMzguMjcgMTUuMzFMMTM2LjY0IDE1LjMxWk0xNTMuMzggMjJMMTQ3LjAwIDIyTDE0Ny4wMCAxMy42MEwxNDkuMzggMTMuNjBMMTQ5LjM4IDIwLjExTDE1My4zOCAyMC4xMUwxNTMuMzggMjJaTTE1OS4yMiAyMkwxNTYuNzkgMjJMMTYwLjUwIDEzLjYwTDE2Mi44NSAxMy42MEwxNjYuNTYgMjJMMTY0LjA5IDIyTDE2My40MyAyMC4zN0wxNTkuODggMjAuMzdMMTU5LjIyIDIyWk0xNjEuNjYgMTUuOTNMMTYwLjU3IDE4LjYxTDE2Mi43NCAxOC42MUwxNjEuNjYgMTUuOTNaTTE3MC4yOSAxNy44MEwxNzAuMjkgMTcuODBRMTcwLjI5IDE2LjU0IDE3MC44OSAxNS41NFExNzEuNDggMTQuNTUgMTcyLjUzIDEzLjk5UTE3My41OSAxMy40MyAxNzQuOTEgMTMuNDNMMTc0LjkxIDEzLjQzUTE3Ni4wNiAxMy40MyAxNzYuOTggMTMuODRRMTc3LjkxIDE0LjI1IDE3OC41MiAxNS4wMkwxNzguNTIgMTUuMDJMMTc3LjAxIDE2LjM5UTE3Ni4xOSAxNS40MCAxNzUuMDMgMTUuNDBMMTc1LjAzIDE1LjQwUTE3NC4zNCAxNS40MCAxNzMuODEgMTUuNzBRMTczLjI4IDE2IDE3Mi45OCAxNi41NFExNzIuNjggMTcuMDkgMTcyLjY4IDE3LjgwTDE3Mi42OCAxNy44MFExNzIuNjggMTguNTEgMTcyLjk4IDE5LjA1UTE3My4yOCAxOS42MCAxNzMuODEgMTkuOTBRMTc0LjM0IDIwLjIwIDE3NS4wMyAyMC4yMEwxNzUuMDMgMjAuMjBRMTc2LjE5IDIwLjIwIDE3Ny4wMSAxOS4yMkwxNzcuMDEgMTkuMjJMMTc4LjUyIDIwLjU4UTE3Ny45MSAyMS4zNSAxNzYuOTkgMjEuNzZRMTc2LjA2IDIyLjE3IDE3NC45MSAyMi4xN0wxNzQuOTEgMjIuMTdRMTczLjU5IDIyLjE3IDE3Mi41MyAyMS42MVExNzEuNDggMjEuMDUgMTcwLjg5IDIwLjA1UTE3MC4yOSAxOS4wNiAxNzAuMjkgMTcuODBaTTE4NS40MSAyMkwxODMuMDYgMjJMMTgzLjA2IDEzLjYwTDE4NS40MSAxMy42MEwxODUuNDEgMTcuMDlMMTg4LjY2IDEzLjYwTDE5MS4yOCAxMy42MEwxODcuODUgMTcuMzJMMTkxLjQ2IDIyTDE4OC43MCAyMkwxODYuMzAgMTguOTVMMTg1LjQxIDE5LjkwTDE4NS40MSAyMloiIGZpbGw9IiNGRkZGRkYiIHg9IjEzMy4xIi8+PC9zdmc+)](https://github.com/psf/black)
[![forthebadge](https://forthebadge.com/images/badges/made-with-python.svg)](https://forthebadge.com)
[![forthebadge](https://forthebadge.com/images/badges/60-percent-of-the-time-works-every-time.svg)](https://forthebadge.com)

## About

This is a script to draw an image onto r/place (<https://www.reddit.com/r/place/>).

## Features

- Support for multiple accounts.
- Determines the cooldown time remaining for each account.
- Detects existing matching pixels on the r/place map and skips them.
- Automatically converts colors to the r/place color palette.
- Easy(ish) to read output with colors.
- SOCKS proxy support.
- No client id and secret needed.
- Proxies from "proxies.txt" file.
- Tor support.

## Requirements

-   [Latest Version of Python 3](https://www.python.org/downloads/)

## MacOSX

If you want to use tor on MacOSX. you'll need to provide your own tor binary and start it manually. deactivate the "use_builtin tor"
option in the config and make sure you configure your tor to use the specified ports and password. 

*Please note that socks proxy connection to tor doesn't work for the time being, so the config value is for an httpTunnel port*

## Get Started

Move the file 'config_example.json' to config.json

Edit the values to replace with actual credentials and values

Note: Please use https://jsonlint.com/ to check that your JSON file is correctly formatted

```json
{
	//Where the image's path is
	"image_path": "image.png",
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

-   Use `.png` if you wish to make use of transparency or non rectangular images
-   If you use 2 factor authentication (2FA) in your account, then change `password` to `password:XXXXXX` where `XXXXXX` is your 2FA code.

## Run the Script

### Windows

```shell
start.bat or startverbose.bat
```

### Unix-like (Linux, MacOS etc.)

```shell
chmod +x start.sh startverbose.sh
./start.sh or ./startverbose.sh
```

**You can get more logs (`DEBUG`) by running the script with `-d` flag:**

`python3 main.py -d` or `python3 main.py --debug`

## Multiple Workers
Just create multiple child arrays to "workers" in the .json file:

```json
{
	"image_path": "image.png",
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

If any JSON decoders errors are found, the `config.json` needs to be fixed. Make sure to add the below 2 lines in the file.

```json
{
	"thread_delay": 2,
	"unverified_place_frequency": false,
	"proxies": ["1.1.1.1:8080", "2.2.2.2:1234"],
	"compact_logging": true
}
```

- thread_delay - Adds a delay between starting a new thread. Can be used to avoid ratelimiting.
- unverified_place_frequency - Sets the pixel place frequency to the unverified account limit.
- proxies - Sets proxies to use for sending requests to reddit. The proxy used is randomly selected for each request. Can be used to avoid ratelimiting.
- compact_logging - Disables timer text until next pixel.
- Transparency can be achieved by using the RGB value (69, 42, 0) in any part of your image.
- If you'd like, you can enable Verbose Mode by adding `--verbose` to "python main.py". This will output a lot more information, and not neccessarily in the right order, but it is useful for development and debugging.
- You can also setup proxies by creating a "proxies" and have a new line for each proxies.

# Tor
Tor can be used as an alternative to normal proxies. Note that currently, you cannot use normal proxies and tor at the same time.

```json
"using_tor": false,
"tor_port": 1881,
"tor_control_port": 9051,
"tor_password": "Passwort",
"tor_delay": 5,
"use_builtin_tor": true
```

The config values are as follows:
- Deactivates or activates tor.
- Sets the httptunnel port that should be used.
- Sets the tor control port.
- Sets the password (leave it as "Passwort" if you want to use the default binaries.
- The delay that tor should receive to process a new connection.
- Whether the included tor binary should be used. It is preconfigured. If you want to use your own binary, make sure you configure it properly.

Note that when using the included binaries, only the tunnel port is explicitly set while starting tor.

<h3>If you want to use your own binaries, follow these steps:</h3>

- Get tor standalone for your platform [here](https://www.torproject.org/download/tor/). For Windows just use the expert bundle. For MacOS you'll have to compile the binaries yourself or get them from somewhere else, which is both out of the scope of this guide.
- In your tor folder, create a file named ``torrc``. Copy [this](https://github.com/torproject/tor/blob/main/src/config/torrc.sample.in) into it.
- Search for ``ControlPort`` in your torrc file and uncomment it. Change the port number to your desired control port.
- Decide on the password you want to use. Run ``tor --hash-password PASSWORD`` from a terminal in the folder with your tor executable, with "PASSWORD" being your desired password. Copy the resulting hash.
- Search for ``HashedControlPassword`` and uncomment it. Paste the hash value you copied after it.
- Decide on a port for your httptunnel. The default for this script is 1881.
- Fill in your password, your httptunnel port and your control port in this script's ``config.json`` and enable tor with ``using_tor = true``.
- To start tor, run ``tor --defaults-torrc PATHTOTORRC --HttpTunnelPort TUNNELPORT``, with PATHTOTORRC being your path to the torrc file you created and TUNNELPORT being your httptunnel port.
- Now run the script and (hopefully) everything should work.

License for the included tor binary:

> Tor is distributed under the "3-clause BSD" license, a commonly used
software license that means Tor is both free software and open source:
Copyright (c) 2001-2004, Roger Dingledine
Copyright (c) 2004-2006, Roger Dingledine, Nick Mathewson
Copyright (c) 2007-2019, The Tor Project, Inc.
Redistribution and use in source and binary forms, with or without
modification, are permitted provided that the following conditions are
met:
>- Redistributions of source code must retain the above copyright
notice, this list of conditions and the following disclaimer.
>- Redistributions in binary form must reproduce the above
copyright notice, this list of conditions and the following disclaimer
in the documentation and/or other materials provided with the
distribution.
>- Neither the names of the copyright owners nor the names of its
contributors may be used to endorse or promote products derived from
this software without specific prior written permission.
>
>THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
"AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR
A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT
OWNER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL,
SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT
LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE,
DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY
THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
(INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

## Docker

A dockerfile is provided. Instructions on installing docker are outside the scope of this guide.

To build: After editing the `config.json` file, run `docker build . -t place-bot`. and wait for the image to build.

You can now run it with `docker run place-bot`

## Contributing

See the [Contributing Guide](docs/CONTRIBUTING.md).
