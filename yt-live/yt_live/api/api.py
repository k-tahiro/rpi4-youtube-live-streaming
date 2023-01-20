import pickle
from datetime import datetime
from pathlib import Path

from google.auth.transport.requests import Request
from google_auth_oauthlib.flow import InstalledAppFlow
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build


class YouTubeAPI:
    SCOPES = ["https://www.googleapis.com/auth/youtube"]

    def __init__(self, api_key: str, credentials: Credentials) -> None:
        self.api_key = api_key
        self.credentials = credentials

        youtube = build("youtube", "v3", developerKey=api_key, credentials=credentials)
        self.live_broadcasts = youtube.liveBroadcasts()

        response = youtube.liveStreams().list(part="id,cdn", mine=True).execute()
        live_stream = response["items"][0]
        self.live_stream_id = live_stream["id"]
        self.stream_url = live_stream["cdn"]["ingestionInfo"]["ingestionAddress"]
        self.stream_key = live_stream["cdn"]["ingestionInfo"]["streamName"]

    @classmethod
    def from_files(
        cls, api_key: str, client_secrets_file: Path, credentials_file: Path
    ) -> "YouTubeAPI":
        return cls(api_key, cls.get_credentials(client_secrets_file, credentials_file))

    @classmethod
    def get_credentials(
        cls, client_secrets_file: Path, credentials_file: Path
    ) -> Credentials:
        if credentials_file.exists():
            with open(credentials_file, "rb") as token:
                credentials = pickle.load(token)

            if credentials.valid:
                return credentials

            if credentials.expired and credentials.refresh_token:
                credentials.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                client_secrets_file, cls.SCOPES
            )
            credentials = flow.run_local_server(open_browser=False)

        with open(credentials_file, "wb") as f:
            pickle.dump(credentials, f)

        return credentials

    def set_up_broadcast(self, title: str, privacy_status: str = "private") -> None:
        response = self.live_broadcasts.insert(
            part="snippet,contentDetails,status",
            body={
                "contentDetails": {
                    "enableAutoStart": True,
                    "enableAutoStop": True,
                    "recordFromStart": True,
                },
                "snippet": {
                    "title": title,
                    # "scheduledStartTime": f"{datetime.utcfromtimestamp(0).isoformat()}Z",
                    "scheduledStartTime": f"{datetime.utcnow().isoformat()}Z",
                },
                "status": {"privacyStatus": privacy_status},
            },
        ).execute()
        self.live_broadcast_id = response["id"]

        self.live_broadcasts.bind(
            part="snippet", id=self.live_broadcast_id, streamId=self.live_stream_id
        ).execute()

    @property
    def output_url(self) -> str:
        return f"{self.stream_url}/{self.stream_key}"

    @property
    def watch_url(self) -> str:
        return f"https://www.youtube.com/watch?v={self.live_broadcast_id}"
