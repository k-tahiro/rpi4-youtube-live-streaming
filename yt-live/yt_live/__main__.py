import os
from logging import basicConfig
from pathlib import Path

import requests
import typer

from .api.api import YouTubeAPI
from .streamer.devices.capture_board import CaptureBoard
from .streamer.devices.usb_mic import UsbMic
from .streamer.streamer import Streamer


def _main(
    title: str,
    privacy_status: str = "unlisted",
    cb_name: str = "MiraBox Capture",
    input_size: str = "480p",
    output_size: str = "480p",
    log_level: str = "INFO",
) -> None:
    basicConfig(level=log_level)

    capture_board = CaptureBoard.from_name(cb_name, input_size)
    usb_mic = UsbMic.from_first_device()

    api_key = os.environ["API_KEY"]
    client_secrets_file = Path(os.environ["CLIENT_SECRETS_FILE"])
    credentials_file = Path(os.getenv("CREDENTIALS_FILE", "token.pickle"))
    youtube = YouTubeAPI.from_files(api_key, client_secrets_file, credentials_file)
    streamer = Streamer(youtube.output_url, output_size)

    youtube.set_up_broadcast(title, privacy_status)
    discord_webhook_url = os.getenv("DISCORD_WEBHOOK_URL")
    if discord_webhook_url:
        requests.post(
            discord_webhook_url,
            json={"content": youtube.message},
        )

    streamer.run(capture_board, usb_mic)


def main() -> None:
    typer.run(_main)


main()
