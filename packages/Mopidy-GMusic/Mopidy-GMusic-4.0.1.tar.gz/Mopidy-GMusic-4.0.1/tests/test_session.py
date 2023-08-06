from unittest import mock

import pytest
import requests

import gmusicapi
from mopidy_gmusic import session as session_lib


@pytest.fixture
def offline_session():
    api_mock = mock.Mock(spec=gmusicapi.Mobileclient)
    api_mock.is_authenticated.return_value = False
    return session_lib.GMusicSession(all_access=True, api=api_mock)


@pytest.fixture
def online_session():
    api_mock = mock.Mock(spec=gmusicapi.Mobileclient)
    api_mock.is_authenticated.return_value = True
    return session_lib.GMusicSession(all_access=True, api=api_mock)


# TODO login


class TestLogout:
    def test_when_offline(self, offline_session):
        assert offline_session.logout() is None

        assert offline_session.api.logout.call_count == 0

    def test_when_online(self, online_session):
        online_session.api.logout.return_value = mock.sentinel.rv

        assert online_session.logout() is mock.sentinel.rv

        online_session.api.logout.assert_called_once_with()

    def test_when_call_failure(self, online_session, caplog):
        online_session.api.logout.side_effect = gmusicapi.CallFailure(
            "foo", "bar"
        )

        assert online_session.logout() is None
        assert "Call to Google Play Music failed" in caplog.text

    def test_when_connection_error(self, online_session, caplog):
        online_session.api.logout.side_effect = (
            requests.exceptions.ConnectionError
        )

        assert online_session.logout() is None
        assert "HTTP request to Google Play Music failed" in caplog.text


class TestGetAllSongs:
    def test_when_offline(self, offline_session):
        assert offline_session.get_all_songs() == []

    def test_when_online(self, online_session):
        online_session.api.get_all_songs.return_value = mock.sentinel.rv

        assert online_session.get_all_songs() is mock.sentinel.rv

        online_session.api.get_all_songs.assert_called_once_with()


class TestGetStreamUrl:
    def test_when_offline(self, offline_session):
        assert offline_session.get_stream_url("abc") is None

    def test_when_online(self, online_session):
        online_session.api.get_stream_url.return_value = mock.sentinel.rv

        assert online_session.get_stream_url("abc") is mock.sentinel.rv

        online_session.api.get_stream_url.assert_called_once_with(
            "abc", quality="hi"
        )


class TestGetAllPlaylists:
    def test_when_offline(self, offline_session):
        assert offline_session.get_all_playlists() == []

    def test_when_online(self, online_session):
        online_session.api.get_all_playlists.return_value = mock.sentinel.rv

        assert online_session.get_all_playlists() is mock.sentinel.rv

        online_session.api.get_all_playlists.assert_called_once_with()


class TestGetAllUserPlaylistContents:
    def test_when_offline(self, offline_session):
        assert offline_session.get_all_user_playlist_contents() == []

    def test_when_online(self, online_session):
        online_session.api.get_all_user_playlist_contents.return_value = (
            mock.sentinel.rv
        )

        assert (
            online_session.get_all_user_playlist_contents() is mock.sentinel.rv
        )

        (
            online_session.api.get_all_user_playlist_contents.assert_called_once_with()
        )


class TestGetSharedPlaylistContents:
    def test_when_offline(self, offline_session):
        assert offline_session.get_shared_playlist_contents("token") == []

    def test_when_online(self, online_session):
        online_session.api.get_shared_playlist_contents.return_value = (
            mock.sentinel.rv
        )

        assert (
            online_session.get_shared_playlist_contents("token")
            is mock.sentinel.rv
        )

        (
            online_session.api.get_shared_playlist_contents.assert_called_once_with(
                "token"
            )
        )


class TestGetTopSongs:
    def test_when_offline(self, offline_session):
        assert offline_session.get_top_songs() == []

    def test_when_online(self, online_session):
        online_session.api.get_top_songs.return_value = mock.sentinel.rv

        assert online_session.get_top_songs() is mock.sentinel.rv

        online_session.api.get_top_songs.assert_called_once_with()


class TestGetTrackInfo:
    def test_when_offline(self, offline_session):
        assert offline_session.get_track_info("id") is None

    def test_when_online(self, online_session):
        online_session.api.get_track_info.return_value = mock.sentinel.rv

        assert online_session.get_track_info("id") is mock.sentinel.rv

        online_session.api.get_track_info.assert_called_once_with("id")

    def test_without_all_access(self, online_session, caplog):
        online_session._all_access = False

        assert online_session.get_track_info("id") is None
        assert (
            "Google Play Music All Access is required for get_track_info()"
            in caplog.text
        )


class TestGetAlbumInfo:
    def test_when_offline(self, offline_session):
        assert offline_session.get_album_info("id") is None

    def test_when_online(self, online_session):
        online_session.api.get_album_info.return_value = mock.sentinel.rv

        result = online_session.get_album_info("id", include_tracks=False)

        assert result is mock.sentinel.rv
        online_session.api.get_album_info.assert_called_once_with(
            "id", include_tracks=False
        )

    def test_without_all_access(self, online_session, caplog):
        online_session._all_access = False

        assert online_session.get_album_info("id") is None
        assert (
            "Google Play Music All Access is required for get_album_info()"
            in caplog.text
        )


class TestGetArtistInfo:
    def test_when_offline(self, offline_session):
        assert offline_session.get_artist_info("id") is None

    def test_when_online(self, online_session):
        online_session.api.get_artist_info.return_value = mock.sentinel.rv

        result = online_session.get_artist_info(
            "id", include_albums=False, max_rel_artist=3, max_top_tracks=4
        )

        assert result is mock.sentinel.rv
        online_session.api.get_artist_info.assert_called_once_with(
            "id", include_albums=False, max_rel_artist=3, max_top_tracks=4
        )

    def test_without_all_access(self, online_session, caplog):
        online_session._all_access = False

        assert online_session.get_artist_info("id") is None
        assert (
            "Google Play Music All Access is required for get_artist_info()"
            in caplog.text
        )


class TestSearchAllAccess:
    def test_when_offline(self, offline_session):
        assert offline_session.search("abba") is None

    def test_when_online(self, online_session):
        online_session.api.search.return_value = mock.sentinel.rv

        result = online_session.search("abba", max_results=10)

        assert result is mock.sentinel.rv
        online_session.api.search.assert_called_once_with(
            "abba", max_results=10
        )

    def test_without_all_access(self, online_session, caplog):
        online_session._all_access = False

        online_session.api.search.return_value = mock.sentinel.rv

        assert online_session.search("abba") is mock.sentinel.rv
        assert "Google Play Music All Access is required for" not in caplog.text


class TestGetAllStations:
    def test_when_offline(self, offline_session):
        assert offline_session.get_all_stations() == [
            {"id": "IFL", "name": "I'm Feeling Lucky"}
        ]

    def test_when_online(self, online_session):
        online_session.api.get_all_stations.return_value = mock.sentinel.rv

        assert online_session.get_all_stations() is mock.sentinel.rv

        online_session.api.get_all_stations.assert_called_once_with()


class TestGetStationTracks:
    def test_when_offline(self, offline_session):
        assert offline_session.get_station_tracks("IFL") == []

    def test_when_online(self, online_session):
        online_session.api.get_station_tracks.return_value = mock.sentinel.rv

        result = online_session.get_station_tracks("IFL", num_tracks=5)

        assert result is mock.sentinel.rv
        online_session.api.get_station_tracks.assert_called_once_with(
            "IFL", num_tracks=5
        )

    def test_without_all_access(self, online_session, caplog):
        online_session._all_access = False

        assert online_session.get_station_tracks("IFL") == []
        assert (
            "Google Play Music All Access is required for get_station_tracks()"
            in caplog.text
        )


class TestIncrementSongPlayCount:
    def test_when_offline(self, offline_session):
        assert offline_session.increment_song_playcount("foo") is None

    def test_when_online(self, online_session):
        online_session.api.increment_song_playcount.return_value = (
            mock.sentinel.rv
        )

        result = online_session.increment_song_playcount(
            "foo", plays=2, playtime=1000000000
        )

        assert result is mock.sentinel.rv
        online_session.api.increment_song_playcount.assert_called_once_with(
            "foo", plays=2, playtime=1000000000
        )
