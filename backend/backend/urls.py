from django.shortcuts import redirect
from django.urls import path, include
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from rest_framework.routers import DefaultRouter
from music.views import ArtistViewSet, AlbumViewSet, SongViewSet

router = DefaultRouter()
router.register(r'artists', ArtistViewSet)
router.register(r'albums', AlbumViewSet)
router.register(r'songs', SongViewSet)

schema_view = get_schema_view(
    openapi.Info(
        title="Music Catalog API",
        default_version='v1',
        description="API для управления исполнителями, альбомами и песнями",
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)


def redirect_to_swagger(request):
    return redirect('schema-swagger-ui')


urlpatterns = [
    path('', redirect_to_swagger),
    path('api/', include(router.urls)),
    path(
        'swagger/',
        schema_view.with_ui('swagger', cache_timeout=0),
        name='schema-swagger-ui',
    ),
    path(
        'redoc/',
        schema_view.with_ui('redoc', cache_timeout=0),
        name='schema-redoc',
    ),
]
