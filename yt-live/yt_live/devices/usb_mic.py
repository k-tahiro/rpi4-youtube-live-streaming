from .base import Device


class UsbMic(Device):
    AUDIO_FMT = "pulse"

    def __init__(self, audio_url: str) -> None:
        super().__init__(audio_fmt=self.AUDIO_FMT, audio_url=audio_url)
