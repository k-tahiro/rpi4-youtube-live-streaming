from .base import Device


class CaptureBoard(Device):
    VIDEO_FMT = "video4linux2"
    VIDEO_INPUT_FMT = "mjpeg"
    AUDIO_FMT = "alsa"
    AUDIO_URL = "hw:CARD=MS2109,DEV=0"

    SIZE_MAPPING = {
        "1080p": "1920x1080",
        "720p": "1280x720",
        "480p": "720x480",
    }

    def __init__(self, video_url: str, video_size: str = "480p") -> None:
        super().__init__(
            self.VIDEO_FMT,
            video_url,
            {
                "input_format": self.VIDEO_INPUT_FMT,
                "video_size": self.SIZE_MAPPING[video_size],
            },
            self.AUDIO_FMT,
            self.AUDIO_URL,
        )

        self.video_size = video_size
