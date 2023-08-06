import logging
import re

from pandora.models.ad import AdItem
from pandora.models.playlist import PlaylistItem
from pandora.models.station import GenreStation, Station
from requests.utils import quote, unquote

from mopidy import models

logger = logging.getLogger(__name__)


def with_metaclass(meta, *bases):
    return meta("NewBase", bases, {})


class _PandoraUriMeta(type):
    def __init__(cls, name, bases, clsdict):  # noqa: N805
        super().__init__(name, bases, clsdict)
        if hasattr(cls, "uri_type"):
            cls.TYPES[cls.uri_type] = cls


class PandoraUri(with_metaclass(_PandoraUriMeta, object)):
    TYPES = {}
    SCHEME = "pandora"

    def __init__(self, uri_type=None):
        self.uri_type = uri_type

    def __repr__(self):
        return "{}:{uri_type}".format(self.SCHEME, **self.__dict__)

    @property
    def encoded_attributes(self):
        encoded_dict = {}
        for k, v in list(self.__dict__.items()):
            encoded_dict[k] = quote(PandoraUri.encode(v))

        return encoded_dict

    @property
    def uri(self):
        return repr(self)

    @classmethod
    def encode(cls, value):
        if value is None:
            value = ""
        if isinstance(value, str):
            value = value.encode("utf-8")
        if isinstance(value, int):
            value = f"{value}"
        return value

    @classmethod
    def factory(cls, obj):
        if isinstance(obj, str):  # noqa: F821
            # A string
            return PandoraUri._from_uri(obj)

        if isinstance(obj, models.Ref) or isinstance(obj, models.Track):
            # A mopidy track or track reference
            return PandoraUri._from_uri(obj.uri)

        elif isinstance(obj, Station) or isinstance(obj, GenreStation):
            # One of the station types
            return PandoraUri._from_station(obj)

        elif isinstance(obj, PlaylistItem) or isinstance(obj, AdItem):
            # One of the playlist item (track) types
            return PandoraUri._from_track(obj)
        else:
            raise NotImplementedError(
                "Unsupported URI object type '{}'".format(type(obj))
            )

    @classmethod
    def _from_uri(cls, uri):
        parts = [unquote(p) for p in uri.split(":")]
        if not parts or parts[0] != PandoraUri.SCHEME or len(parts) < 2:
            raise NotImplementedError(f"Not a Pandora URI: {uri}")
        uri_cls = cls.TYPES.get(parts[1])
        if uri_cls:
            return uri_cls(*parts[2:])
        else:
            raise NotImplementedError(f"Unsupported Pandora URI type '{uri}'")

    @classmethod
    def _from_station(cls, station):
        if isinstance(station, Station) or isinstance(station, GenreStation):
            if (
                GenreStationUri.pattern.match(station.id)
                and station.id == station.token
            ):
                return GenreStationUri(station.id, station.token)
            return StationUri(station.id, station.token)
        else:
            raise NotImplementedError(
                f"Unsupported station item type '{station}'"
            )

    @classmethod
    def _from_track(cls, track):
        if isinstance(track, PlaylistItem):
            return PlaylistItemUri(track.station_id, track.track_token)
        elif isinstance(track, AdItem):
            return AdItemUri(track.station_id, track.ad_token)
        else:
            raise NotImplementedError(
                f"Unsupported playlist item type '{track}'"
            )

    @classmethod
    def is_pandora_uri(cls, uri):
        try:
            return (
                uri
                and isinstance(uri, str)  # noqa: F821
                and uri.startswith(PandoraUri.SCHEME)
                and PandoraUri.factory(uri)
            )
        except NotImplementedError:
            return False


class GenreUri(PandoraUri):
    uri_type = "genre"

    def __init__(self, category_name):
        super().__init__(self.uri_type)
        self.category_name = category_name

    def __repr__(self):
        return "{}:{category_name}".format(
            super().__repr__(), **self.encoded_attributes
        )


class GenresUri(PandoraUri):
    uri_type = "genres"

    def __init__(self):
        super().__init__(self.uri_type)


class StationUri(PandoraUri):
    uri_type = "station"

    def __init__(self, station_id, token):
        super().__init__(self.uri_type)
        self.station_id = station_id
        self.token = token

    def __repr__(self):
        return "{}:{station_id}:{token}".format(
            super().__repr__(), **self.encoded_attributes
        )


class GenreStationUri(StationUri):
    uri_type = "genre_station"
    pattern = re.compile(r"^([G])(\d*)$")  # noqa: W605

    def __init__(self, station_id, token):
        # Check that this really is a Genre station as opposed to a regular station.
        # Genre station IDs and tokens always start with 'G'.

        assert GenreStationUri.pattern.match(station_id)
        assert GenreStationUri.pattern.match(token)
        super().__init__(station_id, token)


class TrackUri(PandoraUri):
    uri_type = "track"


class PlaylistItemUri(TrackUri):
    def __init__(self, station_id, token):
        super().__init__(self.uri_type)
        self.station_id = station_id
        self.token = token

    def __repr__(self):
        return "{}:{station_id}:{token}".format(
            super().__repr__(), **self.encoded_attributes
        )


class AdItemUri(TrackUri):
    uri_type = "ad"

    def __init__(self, station_id, ad_token):
        super().__init__(self.uri_type)
        self.station_id = station_id
        self.ad_token = ad_token

    def __repr__(self):
        return "{}:{station_id}:{ad_token}".format(
            super().__repr__(), **self.encoded_attributes
        )


class SearchUri(PandoraUri):
    uri_type = "search"

    def __init__(self, token):
        super().__init__(self.uri_type)

        # Check that this really is a search result URI as opposed to a regular URI.
        # Search result tokens always start with 'S' (song), 'R' (artist),
        # 'C' (composer), or 'G' (genre station).
        assert re.match("^([SRCG])", token)
        self.token = token

    def __repr__(self):
        return "{}:{token}".format(
            super().__repr__(), **self.encoded_attributes
        )

    @property
    def is_track_search(self):
        return self.token.startswith("S")

    @property
    def is_artist_search(self):
        return self.token.startswith("R")

    @property
    def is_composer_search(self):
        return self.token.startswith("C")

    @property
    def is_genre_search(self):
        return self.token.startswith("G")
