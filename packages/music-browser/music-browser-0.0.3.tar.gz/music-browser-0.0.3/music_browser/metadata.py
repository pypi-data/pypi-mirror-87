from typing import List
from .plugins import Plugin
import music_browser.exceptions

REQUIRED = True
OPTIONAL = False


class TrackMetadataQuery:
    """
    Object used to retrieve requested track metadata, given a few info about the track.
    """

    def __init__(self, plugins: List[Plugin], known_fields=List[str]):
        self.plugins = plugins
        self.known_fields = known_fields

    def query(
        self,
        query_string: str = None,
        title: str = None,
        artist: str = None,
        spotify_id: str = None,
    ):
        """
        Specify known info about tracks that can be used to perform search.
        """
        self.query_string = query_string
        self.spotify_id = spotify_id
        return self

    def fields(self, **query_fields):
        """
        Specify fields that you want to retrieve from this query.

        Keyword Arguments:
            **:
                key -- (str) Name of the field to retrieve
                value -- (bool) Indicates that this field is mandatory (required)
        """
        for query_field, required in query_fields.items():
            if required and not hasattr(self.known_fields, query_field):
                raise music_browser.exceptions.UnknownField("No plugin can resolve required field %s." % query_field)
        self.query_fields = query_fields
        return self

    def result(self):
        """
        Try to fetch a track's requested metadata using plugins.
        Each plugin can partially complete fields of the result.
        For each field, first plugin that returns the field win.
        When all required fields are present in result, returns.
        """

        raise NotImplementedError()
