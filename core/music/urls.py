from django.urls import path

from core.music.views import add_song, get_song, music_chart

app_name = 'music'

urlpatterns = [
    # Music
    path('songs/add/', add_song, name='add-song'),
    path('songs/explore/', music_chart, name='explore-music'),
    path('songs/<song_id>/', get_song, name='get-song'),
]