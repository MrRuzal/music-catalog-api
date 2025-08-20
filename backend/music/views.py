from rest_framework import viewsets, filters
from django_filters.rest_framework import DjangoFilterBackend
from .models import Artist, Album, Song
from .serializers import (
    ArtistSerializer,
    AlbumReadSerializer,
    AlbumWriteSerializer,
    SongSerializer,
)
from .pagination import StandardPagination


class ArtistViewSet(viewsets.ModelViewSet):
    '''ViewSet для работы с исполнителями'''

    queryset = Artist.objects.prefetch_related(
        'albums__album_songs__song'
    ).all()
    serializer_class = ArtistSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    search_fields = ['name']
    filterset_fields = ['name']
    pagination_class = StandardPagination


class AlbumViewSet(viewsets.ModelViewSet):
    '''ViewSet для работы с альбомами'''

    queryset = (
        Album.objects.select_related('artist')
        .prefetch_related('album_songs__song')
        .all()
    )
    pagination_class = StandardPagination
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    search_fields = ['title']
    filterset_fields = ['artist__name']

    def get_serializer_class(self):
        if self.request.method in ['GET', 'HEAD', 'OPTIONS']:
            return AlbumReadSerializer
        return AlbumWriteSerializer


class SongViewSet(viewsets.ModelViewSet):
    '''ViewSet для работы с песнями'''

    queryset = Song.objects.select_related('album__artist').all()
    serializer_class = SongSerializer
    pagination_class = StandardPagination
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    search_fields = ['title']
    filterset_fields = ['album__title', 'album__artist__name']

    def get_serializer_class(self):
        if self.request.method in ['GET', 'HEAD', 'OPTIONS']:
            return SongSerializer
        return SongSerializer
