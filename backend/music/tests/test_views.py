from rest_framework.test import APITestCase
from rest_framework import status
from music.models import Artist, Song, Album
from django.utils import timezone


class AlbumAPITest(APITestCase):
    def setUp(self):
        self.artist = Artist.objects.create(name="Test Artist")
        self.song1 = Song.objects.create(title="Song 1")
        self.song2 = Song.objects.create(title="Song 2")

    def test_create_album(self):
        data = {
            "title": "Best Hits",
            "artist": self.artist.id,
            "release_year": timezone.now().year,
            "track_data": [
                {"track_number": 1, "song": self.song1.id},
                {"track_number": 2, "song": self.song2.id},
            ],
        }
        response = self.client.post("/api/albums/", data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Album.objects.count(), 1)

    def test_list_albums(self):
        album = Album.objects.create(
            title="Existing Album",
            artist=self.artist,
            release_year=timezone.now().year,
        )
        response = self.client.get("/api/albums/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertGreaterEqual(len(response.data), 1)

    def test_update_album(self):
        album = Album.objects.create(
            title="Old Album", artist=self.artist, release_year=2024
        )
        data = {
            "title": "Updated Album",
            "artist": self.artist.id,
            "release_year": 2025,
            "track_data": [{"track_number": 1, "song": self.song1.id}],
        }
        response = self.client.put(
            f"/api/albums/{album.id}/", data, format="json"
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        album.refresh_from_db()
        self.assertEqual(album.title, "Updated Album")

    def test_delete_album(self):
        album = Album.objects.create(
            title="Delete Album", artist=self.artist, release_year=2024
        )
        response = self.client.delete(f"/api/albums/{album.id}/")
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Album.objects.count(), 0)
