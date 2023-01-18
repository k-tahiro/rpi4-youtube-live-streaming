from logging import basicConfig
from typing import Optional

import typer

from .devices.capture_board import CaptureBoard
from .devices.usb_mic import UsbMic
from .youtube_live import YouTubeLive


def _main(
    stream_key: str,  # TODO: Get stream key and start live automatically
    video_url: str,
    input_size: str = "480p",
    output_size: str = "480p",
    audio_url: Optional[str] = None,
    log_level: str = "INFO",
) -> None:
    basicConfig(level=log_level)

    capture_board = CaptureBoard(video_url, input_size)
    usb_mic = UsbMic(audio_url) if audio_url is not None else None

    youtube_live = YouTubeLive(stream_key, output_size)
    youtube_live.run(capture_board, usb_mic)


def main() -> None:
    typer.run(_main)


main()
