from typing import Optional

import ffmpeg


class Device:
    def __init__(
        self,
        video_fmt: Optional[str] = None,
        video_url: Optional[str] = None,
        video_kwargs: Optional[dict] = None,
        audio_fmt: Optional[str] = None,
        audio_url: Optional[str] = None,
        audio_kwargs: Optional[dict] = None,
        **kwargs,
    ) -> None:
        self.video_fmt = video_fmt
        self.video_url = video_url
        self.video_kwargs = video_kwargs
        self.audio_fmt = audio_fmt
        self.audio_url = audio_url
        self.audio_kwargs = audio_kwargs

    @property
    def vstream(self) -> ffmpeg.Stream:
        video_kwargs = self.video_kwargs or {}
        return ffmpeg.input(self.video_url, f=self.video_fmt, **video_kwargs)

    @property
    def astream(self) -> ffmpeg.Stream:
        audio_kwargs = self.audio_kwargs or {}
        return ffmpeg.input(self.audio_url, f=self.audio_fmt, **audio_kwargs)
