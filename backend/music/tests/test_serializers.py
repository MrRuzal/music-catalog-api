from django.test import TestCase
from music.models import Artist, Album, Song
from music.serializers import AlbumWriteSerializer
from django.utils import timezone


class AlbumSerializerTest(TestCase):
    def setUp(self):
        self.artist = Artist.objects.create(name="Test Artist")
        self.song1 = Song.objects.create(title="Song 1")
        self.song2 = Song.objects.create(title="Song 2")

    def test_album_serializer_valid(self):
        data = {
            "title": "Best Hits",
            "artist": self.artist.id,
            "release_year": timezone.now().year,
            "track_data": [
                {"track_number": 1, "song": self.song1.id},
                {"track_number": 2, "song": self.song2.id},
            ],
        }
        serializer = AlbumWriteSerializer(data=data)
        self.assertTrue(serializer.is_valid(), serializer.errors)

    def test_album_serializer_empty_track_data(self):
        data = {
            "title": "Album Empty",
            "artist": self.artist.id,
            "release_year": timezone.now().year,
            "track_data": [],
        }
        serializer = AlbumWriteSerializer(data=data)
        self.assertFalse(serializer.is_valid())
        self.assertIn('track_data', serializer.errors)

    def test_album_serializer_duplicate_tracks(self):
        data = {
            "title": "Album Duplicate",
            "artist": self.artist.id,
            "release_year": timezone.now().year,
            "track_data": [
                {"track_number": 1, "song": self.song1.id},
                {"track_number": 1, "song": self.song2.id},
            ],
        }
        serializer = AlbumWriteSerializer(data=data)
        self.assertFalse(serializer.is_valid())
        self.assertIn('track_data', serializer.errors)
