from logging import basicConfig

import typer

from .streamer.devices.capture_board import CaptureBoard
from .streamer.devices.usb_mic import UsbMic
from .streamer.youtube_live import YouTubeLive


def _main(
    stream_key: str,  # TODO: Get stream key and start live automatically
    cb_name: str = "MiraBox Capture",
    input_size: str = "480p",
    output_size: str = "480p",
    log_level: str = "INFO",
) -> None:
    basicConfig(level=log_level)

    capture_board = CaptureBoard.from_name(cb_name, input_size)
    usb_mic = UsbMic.from_first_device()

    youtube_live = YouTubeLive(stream_key, output_size)
    youtube_live.run(capture_board, usb_mic)


def main() -> None:
    typer.run(_main)


main()
