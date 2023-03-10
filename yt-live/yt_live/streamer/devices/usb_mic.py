import subprocess
from typing import Optional

from .base import Device


class UsbMic(Device):
    AUDIO_FMT = "pulse"

    def __init__(self, audio_url: str) -> None:
        super().__init__(audio_fmt=self.AUDIO_FMT, audio_url=audio_url)

    @classmethod
    def from_first_device(cls) -> Optional["UsbMic"]:
        cp = subprocess.run(
            ["pactl", "list", "short", "sources"], capture_output=True, text=True
        )
        lines = cp.stdout.splitlines()
        for line in lines:
            if "monitor" not in line:
                audio_url = line.strip().split()[1].strip()
                break
        else:
            return None

        return cls(audio_url)
