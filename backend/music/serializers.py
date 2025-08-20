from rest_framework import serializers
from .models import Artist, Album, Song, AlbumSong
from .validators import (
    ReleaseYearValidator,
    TrackNumberValidator,
)


class SongSerializer(serializers.ModelSerializer):
    '''Сериализатор для модели "Песня"'''

    class Meta:
        model = Song
        fields = ['id', 'title']


class AlbumSongReadSerializer(serializers.ModelSerializer):
    '''Сериализатор для чтения треков альбома'''

    song = SongSerializer()
    track_number = serializers.IntegerField(
        validators=[TrackNumberValidator()]
    )

    class Meta:
        model = AlbumSong
        fields = ['track_number', 'song']


class AlbumSongWriteSerializer(serializers.ModelSerializer):
    '''Сериализатор для записи/обновления треков альбома'''

    song = serializers.PrimaryKeyRelatedField(queryset=Song.objects.all())
    track_number = serializers.IntegerField(
        validators=[TrackNumberValidator()]
    )

    class Meta:
        model = AlbumSong
        fields = ['track_number', 'song']


class AlbumReadSerializer(serializers.ModelSerializer):
    '''Сериализатор для чтения модели "Альбом"'''

    artist = serializers.StringRelatedField()
    tracks = AlbumSongReadSerializer(
        source='album_songs', many=True, read_only=True
    )

    class Meta:
        model = Album
        fields = [
            'id',
            'title',
            'artist',
            'release_year',
            'tracks',
        ]


class AlbumWriteSerializer(serializers.ModelSerializer):
    '''Сериализатор для записи/обновления модели "Альбом"'''

    track_data = AlbumSongWriteSerializer(
        source='album_songs',
        many=True,
        write_only=True,
    )
    release_year = serializers.IntegerField(
        validators=[ReleaseYearValidator()]
    )

    class Meta:
        model = Album
        fields = [
            'id',
            'title',
            'artist',
            'release_year',
            'track_data',
        ]

    def validate_track_data(self, value):
        if not value:
            raise serializers.ValidationError("Track data cannot be empty.")
        track_numbers = set()
        songs = set()
        for item in value:
            track_number = item.get('track_number')
            song = item.get('song')
            if track_number in track_numbers:
                raise serializers.ValidationError(
                    "Duplicate track_number found."
                )
            if song in songs:
                raise serializers.ValidationError("Duplicate song found.")
            track_numbers.add(track_number)
            songs.add(song)
        return value

    def create(self, validated_data):
        album_songs_data = validated_data.pop('album_songs', [])
        album = Album.objects.create(**validated_data)
        album_songs = [
            AlbumSong(album=album, **track_data)
            for track_data in album_songs_data
        ]
        AlbumSong.objects.bulk_create(album_songs)
        return album

    def update(self, instance, validated_data):
        album_songs_data = validated_data.pop('album_songs', [])
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()

        instance.album_songs.all().delete()
        album_songs = [
            AlbumSong(album=instance, **track_data)
            for track_data in album_songs_data
        ]
        if album_songs:
            AlbumSong.objects.bulk_create(album_songs)

        return instance


class ArtistSerializer(serializers.ModelSerializer):
    '''Сериализатор для модели "Исполнитель"'''

    albums = serializers.SerializerMethodField()

    class Meta:
        model = Artist
        fields = ['id', 'name', 'albums']

    def get_albums(self, obj):
        albums_qs = getattr(obj, 'prefetched_albums', None)
        if albums_qs is None:
            albums_qs = obj.albums.prefetch_related('album_songs__song')
        serializer = AlbumReadSerializer(albums_qs, many=True)
        return serializer.data
