from datetime import date
from logging import basicConfig
from pathlib import Path

import typer

from .api.api import YouTubeAPI
from .streamer.devices.capture_board import CaptureBoard
from .streamer.devices.usb_mic import UsbMic
from .streamer.streamer import Streamer


def _main(
    title: str = f"{date.today()}",
    api_key: str = "dummy",
    client_secrets_file: Path = Path("client_secret.json"),
    credentials_file: Path = Path("token.pickle"),
    cb_name: str = "MiraBox Capture",
    input_size: str = "480p",
    output_size: str = "480p",
    log_level: str = "INFO",
) -> None:
    basicConfig(level=log_level)

    capture_board = CaptureBoard.from_name(cb_name, input_size)
    usb_mic = UsbMic.from_first_device()

    youtube = YouTubeAPI.from_files(api_key, client_secrets_file, credentials_file)
    streamer = Streamer(youtube.stream_url, youtube.stream_key, output_size)

    youtube.set_up_broadcast(title)
    streamer.run(capture_board, usb_mic)


def main() -> None:
    typer.run(_main)


main()
