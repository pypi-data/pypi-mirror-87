import requests
from typing import List
from urllib.parse import urlencode
from .base import Plugin
from ..models import SimpleTrack


class DeezerPlugin(Plugin):
    @property
    def known_fields(self):
        return set()

    def query(self):
        pass

    def search(self, query) -> List[SimpleTrack]:
        response = requests.get("https://api.deezer.com/search?" + urlencode({"q": query}))

        tracks = []
        for track_data in response.json()["data"]:
            tracks.append(
                SimpleTrack(
                    album=track_data["album"]["title"],
                    artist=track_data["artist"]["name"],
                    title=track_data["title"],
                    cover="https://e-cdns-images.dzcdn.net/images/cover/%s/264x264-000000-80-0-0.jpg"
                    % track_data["md5_image"],
                    source={"id": str(track_data["id"]), "platform": "deezer"},
                )
            )

        return tracks
