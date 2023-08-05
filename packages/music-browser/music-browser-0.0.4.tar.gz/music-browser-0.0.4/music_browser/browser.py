from typing import List
from .models import SimpleTrack
from .metadata import TrackMetadataQuery


class MusicBrowser:
    """
    Object that abstract plugins usage to query tracks metadata from multiple sources.

    Keywords Arguments:
        plugins -- (list) Plugins ordered by priority used to fetch metadata.
    """

    def __init__(self, search_plugin=None, completion_plugins=None):
        self.search_plugin = search_plugin
        self.plugins = []
        self.known_fields = set()

        if completion_plugins:
            # register plugins that improve MusicBrowser sources
            for plugin_module in completion_plugins:
                self.use_plugin(plugin_module)

    def query(self, query_string=None, title=None, artist=None, spotify_id=None):
        """
        Keywords Arguments:
            query_string -- (str) What you would type in a browser to search this track.
            title -- (str) Title of the track.
            artist -- (str) Name of the artist who created this track.

        Returns:
            track_query -- An object used to do lazy loading of tracks metadata.
        """
        return TrackMetadataQuery(self.plugins).query(
            query_string=query_string, title=title, artist=artist, spotify_id=spotify_id
        )

    def search(self, query: str) -> List[SimpleTrack]:
        """
        Use search_plugin to retrieve a list of tracks.
        """
        return self.search_plugin.search(query)

    def use_plugin(self, plugin):
        """
        Declare the use of the plugin.
        """
        self.plugins.append(plugin)

        for field in plugin.known_fields:
            self.known_fields.add(field)
