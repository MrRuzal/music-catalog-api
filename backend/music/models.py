# models.py
from django.db import models
from django.core.validators import MinValueValidator
from django.utils import timezone
from django.core.exceptions import ValidationError


class Artist(models.Model):
    """Модель исполнителя"""

    name = models.CharField(
        max_length=255,
        unique=True,
        verbose_name="Имя исполнителя",
        help_text="Полное имя или название музыкальной группы",
    )

    class Meta:
        ordering = ["name"]
        verbose_name = "Исполнитель"
        verbose_name_plural = "Исполнители"

    def __str__(self):
        return self.name


class Album(models.Model):
    """Модель альбома"""

    artist = models.ForeignKey(
        Artist,
        on_delete=models.CASCADE,
        related_name="albums",
        verbose_name="Исполнитель",
    )
    title = models.CharField(max_length=255, verbose_name="Название альбома")
    release_year = models.PositiveIntegerField(
        verbose_name="Год выпуска",
        help_text="Год официального релиза альбома",
        validators=[
            MinValueValidator(1900, message="Год не может быть раньше 1900"),
        ],
    )

    class Meta:
        ordering = ["-release_year", "title"]
        verbose_name = "Альбом"
        verbose_name_plural = "Альбомы"
        unique_together = ("artist", "title")

    def clean(self):
        super().clean()
        current_year = timezone.now().year
        if self.release_year > current_year + 1:
            raise ValidationError(
                {'release_year': "Год не может быть более чем на 1 год вперед"}
            )

    def __str__(self):
        return f"{self.title} ({self.artist.name}, {self.release_year})"


class Song(models.Model):
    """Модель песни"""

    title = models.CharField(
        max_length=255, verbose_name="Название песни", db_index=True
    )
    albums = models.ManyToManyField(
        Album,
        through='AlbumSong',
        related_name='songs',
        verbose_name="Альбомы",
    )

    class Meta:
        ordering = ["title"]
        verbose_name = "Песня"
        verbose_name_plural = "Песни"

    def __str__(self):
        return self.title


class AlbumSong(models.Model):
    """Промежуточная модель для связи альбомов и песен"""

    album = models.ForeignKey(
        Album,
        on_delete=models.CASCADE,
        related_name="album_songs",
        verbose_name="Альбом",
    )
    song = models.ForeignKey(
        Song,
        on_delete=models.CASCADE,
        related_name="song_albums",
        verbose_name="Песня",
    )
    track_number = models.PositiveIntegerField(
        verbose_name="Порядковый номер",
        help_text="Позиция песни в альбоме",
        validators=[MinValueValidator(1)],
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["album", "track_number"],
                name="unique_album_track_number",
            ),
            models.UniqueConstraint(
                fields=["album", "song"], name="unique_album_song"
            ),
        ]
        ordering = ["album", "track_number"]
        verbose_name = "Песня в альбоме"
        verbose_name_plural = "Песни в альбомах"

    def __str__(self):
        return f"{self.track_number}. {self.song.title} — {self.album.title}"
