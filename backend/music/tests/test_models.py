from django.test import TestCase
from music.models import Artist, Album, Song, AlbumSong
from django.core.exceptions import ValidationError
from django.utils import timezone


class ArtistModelTest(TestCase):
    def test_create_artist(self):
        artist = Artist.objects.create(name="Test Artist")
        self.assertEqual(str(artist), "Test Artist")


class AlbumModelTest(TestCase):
    def setUp(self):
        self.artist = Artist.objects.create(name="Test Artist")

    def test_create_album(self):
        album = Album.objects.create(
            artist=self.artist,
            title="Test Album",
            release_year=timezone.now().year,
        )
        self.assertEqual(
            str(album),
            f"Test Album ({self.artist.name}, {timezone.now().year})",
        )


class SongModelTest(TestCase):
    def test_create_song(self):
        song = Song.objects.create(title="Test Song")
        self.assertEqual(str(song), "Test Song")


class AlbumSongModelTest(TestCase):
    def setUp(self):
        self.artist = Artist.objects.create(name="Test Artist")
        self.album = Album.objects.create(
            artist=self.artist,
            title="Test Album",
            release_year=timezone.now().year,
        )
        self.song = Song.objects.create(title="Test Song")

    def test_create_album_song(self):
        album_song = AlbumSong.objects.create(
            album=self.album, song=self.song, track_number=1
        )
        self.assertEqual(
            str(album_song), f"1. {self.song.title} — {self.album.title}"
        )
