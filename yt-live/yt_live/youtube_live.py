from logging import getLogger
from typing import NamedTuple, Optional

import ffmpeg

from .devices.capture_board import CaptureBoard
from .devices.usb_mic import UsbMic

logger = getLogger(__name__)


class VideoEncoding(NamedTuple):
    size: str
    bitrate: str
    codec: str = "h264_omx"


class YouTubeLive:
    STREAM_URL = "rtmp://a.rtmp.youtube.com/live2"
    VIDEO_ENCODING_MAPPING = {
        "720p": VideoEncoding("1280x720", "4000k"),
        "480p": VideoEncoding("854x480", "2000k"),
        "360p": VideoEncoding("640x360", "1000k"),
        "240p": VideoEncoding("426x240", "700k"),
    }
    AUDIO_CODEC = "aac"
    AUDIO_SAMPLE_RATE = "44.1k"
    AUDIO_BITRATE = "128k"

    def __init__(
        self,
        stream_key: str,
        video_encoding_key: str = "480p",
    ) -> None:
        self.stream_key = stream_key
        self.video_encoding_key = video_encoding_key

        video_encoding = self.VIDEO_ENCODING_MAPPING[video_encoding_key]
        self.video_size, self.video_bitrate, self.video_codec = video_encoding

    @property
    def output(self) -> str:
        return f"{self.STREAM_URL}/{self.stream_key}"

    def run(
        self, capture_board: CaptureBoard, usb_mic: Optional[UsbMic] = None
    ) -> None:
        if usb_mic is not None:
            astream = ffmpeg.filter(
                [capture_board.astream, usb_mic.astream],
                "amix",
                inputs=2,
                duration="longest",
                dropout_transition=0,
                weights="0.33 1",
            )
        else:
            astream = capture_board.astream

        stream = ffmpeg.output(
            capture_board.vstream,
            astream,
            self.output,
            video_bitrate=self.video_bitrate,
            audio_bitrate=self.AUDIO_BITRATE,
            format="flv",
            fpsmax=60,
            s=self.video_size,
            vcodec=self.video_codec,
            ar=self.AUDIO_SAMPLE_RATE,
            acodec=self.AUDIO_CODEC,
        )

        logger.info(capture_board.vstream)
        logger.info(astream)
        logger.info(stream)

        ffmpeg.run(stream)
