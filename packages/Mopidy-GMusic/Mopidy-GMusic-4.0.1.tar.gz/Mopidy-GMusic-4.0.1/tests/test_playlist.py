import unittest
from unittest import mock

from mopidy.models import Playlist, Ref, Track
from mopidy_gmusic.playlists import GMusicPlaylistsProvider

from tests.test_extension import ExtensionTest


class PlaylistsTest(unittest.TestCase):
    def setUp(self):
        backend = mock.Mock()
        backend.config = ExtensionTest.get_config()
        self.provider = GMusicPlaylistsProvider(backend)
        self.provider._playlists = {
            "gmusic:playlist:foo": Playlist(
                uri="gmusic:playlist:foo",
                name="foo",
                tracks=[Track(uri="gmusic:track:test_track", name="test")],
            ),
            "gmusic:playlist:boo": Playlist(
                uri="gmusic:playlist:boo", name="boo", tracks=[]
            ),
        }

    def test_as_list(self):
        result = self.provider.as_list()

        assert len(result) == 2
        assert result[0] == Ref.playlist(uri="gmusic:playlist:boo", name="boo")
        assert result[1] == Ref.playlist(uri="gmusic:playlist:foo", name="foo")

    def test_get_items(self):
        result = self.provider.get_items("gmusic:playlist:foo")

        assert len(result) == 1
        assert result[0] == Ref.track(
            uri="gmusic:track:test_track", name="test"
        )

    def test_get_items_for_unknown_playlist(self):
        result = self.provider.get_items("gmusic:playlist:bar")

        assert result is None

    def test_create(self):
        with self.assertRaises(NotImplementedError):
            self.provider.create("foo")

    def test_delete(self):
        with self.assertRaises(NotImplementedError):
            self.provider.delete("gmusic:playlist:foo")

    def test_save(self):
        with self.assertRaises(NotImplementedError):
            self.provider.save(Playlist())

    def test_lookup_valid(self):
        result = self.provider.lookup("gmusic:playlist:foo")

        assert result is not None

    def test_lookup_invalid(self):
        result = self.provider.lookup("gmusic:playlist:bar")

        assert result is None
