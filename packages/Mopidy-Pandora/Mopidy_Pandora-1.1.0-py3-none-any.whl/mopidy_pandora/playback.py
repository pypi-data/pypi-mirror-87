import logging

import requests

from mopidy import backend
from mopidy_pandora import listener
from mopidy_pandora.uri import PandoraUri, StationUri

logger = logging.getLogger(__name__)


class PandoraPlaybackProvider(backend.PlaybackProvider):
    SKIP_LIMIT = 5

    def __init__(self, audio, backend):
        super().__init__(audio, backend)

        # TODO: It shouldn't be necessary to keep track of the number of tracks
        # that have been skipped in the player anymore once
        # https://github.com/mopidy/mopidy/issues/1221 has been fixed.
        self._consecutive_track_skips = 0

        # TODO: add gapless playback when it is supported in Mopidy > 1.1
        # self.audio.set_about_to_finish_callback(self.callback)

        # def callback(self):
        # See: https://discourse.mopidy.com/t/784/2
        # self.audio.set_uri(self.translate_uri(self.get_next_track()))

    def change_pandora_track(self, track):
        """Attempt to retrieve the Pandora playlist item from the buffer and
        verify that it is ready to be played.

        A track is playable if it has been stored in the buffer, has a URL, and
        the header for the Pandora URL can be retrieved and the status code
        checked.

        :param track: the track to retrieve and check the Pandora playlist item for.
        :return: True if the track is playable, False otherwise.
        """
        try:
            pandora_track = self.backend.library.lookup_pandora_track(track.uri)
            if pandora_track.get_is_playable():
                # Success, reset track skip counter.
                self._consecutive_track_skips = 0
            else:
                raise Unplayable(
                    f"Track with URI '{track.uri}' is not playable."
                )

        except (
            AttributeError,
            requests.exceptions.RequestException,
            Unplayable,
        ) as e:
            # Track is not playable.
            self._consecutive_track_skips += 1
            self.check_skip_limit()
            self._trigger_track_unplayable(track)
            raise Unplayable(f"Error changing Pandora track: {track}, ({e})")

    def change_track(self, track):
        if track.uri is None:
            logger.warning(
                "No URI for Pandora track '{}'. Track cannot be played.".format(
                    track
                )
            )
            return False

        pandora_uri = PandoraUri.factory(track.uri)
        if isinstance(pandora_uri, StationUri):
            # Change to first track in station playlist.
            logger.warning(
                "Cannot play Pandora stations directly. "
                f"Retrieving tracks for station with ID: {pandora_uri.station_id}"
            )
            self.backend.end_of_tracklist_reached(
                station_id=pandora_uri.station_id, auto_play=True
            )
            return False
        try:
            self._trigger_track_changing(track)
            self.check_skip_limit()
            self.change_pandora_track(track)
            return super().change_track(track)

        except KeyError:
            logger.exception(
                f"Error changing Pandora track: failed to lookup {track.uri!r}"
            )
            return False
        except (MaxSkipLimitExceeded, Unplayable) as e:
            logger.warning(e)
            return False

    def check_skip_limit(self):
        if self._consecutive_track_skips >= self.SKIP_LIMIT:
            self._trigger_skip_limit_exceeded()
            raise MaxSkipLimitExceeded(
                f"Maximum track skip limit ({self.SKIP_LIMIT}) exceeded."
            )

    def reset_skip_limits(self):
        self._consecutive_track_skips = 0

    def translate_uri(self, uri):
        return self.backend.library.lookup_pandora_track(uri).audio_url

    def _trigger_track_changing(self, track):
        listener.PandoraPlaybackListener.send("track_changing", track=track)

    def _trigger_track_unplayable(self, track):
        listener.PandoraPlaybackListener.send("track_unplayable", track=track)

    def _trigger_skip_limit_exceeded(self):
        listener.PandoraPlaybackListener.send("skip_limit_exceeded")


class MaxSkipLimitExceeded(Exception):
    pass


class Unplayable(Exception):
    pass
