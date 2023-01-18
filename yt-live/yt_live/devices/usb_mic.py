import subprocess

from .base import Device


class UsbMic(Device):
    AUDIO_FMT = "pulse"

    def __init__(self, audio_url: str) -> None:
        super().__init__(audio_fmt=self.AUDIO_FMT, audio_url=audio_url)

    @classmethod
    def from_name(cls, name: str) -> "UsbMic":
        cp = subprocess.run(
            ["pactl", "list", "short", "sources"], capture_output=True, text=True
        )
        lines = cp.stdout.splitlines()
        for i, line in enumerate(lines):
            if name in line:
                audio_url = line.strip().split()[1].strip()
                break
        else:
            raise RuntimeError(f'Unable to find "{name}" device')

        return cls(audio_url)
