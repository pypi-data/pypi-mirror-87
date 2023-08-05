import time
import requests
from base64 import b64encode
from typing import List
from urllib.parse import urlencode
from .base import Plugin
from ..models import SimpleTrack
from ..exceptions import MusicBrowserException


class SpotifyAuthentication:
    """
    Manage token based authentication for Spotify Plugin.
    """

    def __init__(self, client_id, client_secret):
        # workout base64 header required by spotify to authenticate using client credentials.
        self.basic_token = b64encode(("%s:%s" % (client_id, client_secret)).encode("utf-8")).decode("utf-8")
        # token lazy loading. Indicates that a new token must be issued from now.
        self.expires = time.time()

    def authenticate(self):
        # exchange client credentials for a token against spotify accounts API.
        response = requests.post(
            "https://accounts.spotify.com/api/token",
            data={"grant_type": "client_credentials"},
            headers={
                "Authorization": "Basic %s" % self.basic_token,
                "Content-Type": "application/x-www-form-urlencoded",
            },
        )
        # ensure that proper token response has been received
        if response.status_code != 200:
            raise MusicBrowserException("Unable to retrieve access_token from Spotify API.")

        token_data = response.json()
        # store useful token data as properties
        self.access_token = token_data["access_token"]
        self.expires = time.time() + token_data["expires_in"]

    def has_expired(self):
        # check if expiration time is passed
        return self.expires < time.time()

    def get_token(self):
        # ensure that known token is up-to-date
        if self.has_expired():
            self.authenticate()
        # ... then return valid access token
        return self.access_token


class SpotifyPlugin(Plugin):
    """
    Define methods to search tracks on spotify
    and complete metadata from spotify's database.
    """

    def __init__(self, client_id, client_secret):
        self.auth = SpotifyAuthentication(client_id, client_secret)

    @property
    def known_fields(self):
        return {"title", "artist", "album"}

    def query(self, query_params, query_fields):
        pass

    def search(self, query) -> List[SimpleTrack]:
        r = requests.get(
            "https://api.spotify.com/v1/search?" + urlencode({"type": "track", "query": query}),
            headers={"Authorization": "Bearer %s" % self.auth.get_token()},
        )

        tracks = []

        for track_data in r.json()["tracks"]["items"]:
            tracks.append(
                SimpleTrack(
                    album=track_data["album"]["name"],
                    artist=track_data["artists"][0]["name"],
                    title=track_data["name"],
                    cover=track_data["album"]["images"][0]["url"],
                    source={"id": track_data["id"], "platform": "spotify"},
                )
            )

        return tracks
