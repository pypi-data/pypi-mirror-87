# Python Music-Browser

> A lightweight and modular python library to query tracks and their metadata from various sources.

- [Plugins features](#plugins-features)
  - [Browse tracks](#browse-tracks)
  - [Complete track metadata](#complete-track-metadata)
- [Make your own plugin](#make-your-own-plugin)
- [Objects structure](#objects-structure)
  - [SimpleTrack](#simpletrack)
  - [FullTrack](#fulltrack)
- [Roadmap](#roadmap)
- [Changelog](#changelog)

## Plugins features

### Browse tracks

You can use plugin to issue any tracks provider (like Spotify) a query.

```python
from music_browser.plugins import SpotifyPlugin

spotify = SpotifyPlugin(
    client_id="97e316da02e94644b332c3ad77554c68", client_secret="9b999c62cf324a428a335a7d87b3d0a9"
)
tracks = spotify.search(query)

for simple_track in tracks:
    print(simple_track)
```

As a result you will get a list of [SimpleTrack](#simpletrack), an object containing most basic properties of a track.

### Complete track metadata

Coming soon...

## Make your own plugin

First of all, your plugin should inherit from the `Plugin` base class.
You will have to implement the following methods.

```python
from typing import List, Set
from music_browser.plugins import Plugin
from music_browser.models import SimpleTrack, FullTrack


class DeezerPlugin(Plugin):
    @property
    def known_fields(self) -> Set[str]:
        # indicates list of field that your plugin can return
        return {"title", "artist", "album"}

    def complete(self, simple_track) -> FullTrack:
        # workout full track properties
        return FullTrack(...)

    def search(self, query) -> List[SimpleTrack]:
        # workout search results
        return [SimpleTrack(...), ..., SimpleTrack(...)]
```

## Objects structure

### SimpleTrack

A [SimpleTrack](#simpletrack) object has the following structure. It is returned when a list of tracks is asked to give a quick preview of each track. If later you would like to query more details, refere to [FullTrack](#fulltrack).

```python
simple_track.__json__()
{
    "title": "Lovers On the Sun (Metal Version)",
    "artist": "UMC",
    "album": "Lovers On the Sun (Metal Version)",
    "cover": "https://i.scdn.co/image/ab67616d0000b273fa786b81f34442a68738be05",
    "source": {
        "id": "5fVCKGCQcZ1VPJNZrWqCO0",
        "platform": "spotify"
    }
},
```

### FullTrack

Coming soon...

## Roadmap

* Add ability to search in SoundCloud by adding a new plugin.
* Prototype advanced metadata-completion for a SimpleTrack.
* Study ability to use multiple search_plugins at once in browser.
* Study where cache would be interesting to optimise performances.

## Changelog

**[0.0.4](https://pypi.org/project/music-browser/0.0.4/) Document package (2020-11-30)**

- Add users and contributors documentation to README.
- Add commons metadata used by PyPI.
- Add licensing information.

**[0.0.3](https://pypi.org/project/music-browser/0.0.3/) First release (2020-11-30)**

- Initiate plugins structure.
- Add search feature for `Spotify` and `Deezer` plugins.
- First attempt to specify plugin interface
- Setup CI/CD for the project
  -  Simple integration on `master` and `integration` branches.
  -  Full integration before release, testing all supported python versions.
