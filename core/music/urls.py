from django.urls import path

from core.music.views import (
    add_song, 
    get_genre, 
    get_song, 
    music_chart
)

app_name = 'music'

urlpatterns = [
    # Music
    path('add/', add_song, name='add-song'),
    path('explore/', music_chart, name='explore-music'),
    path('genre/<genre>/', get_genre, name='get-genre'),
    path('<song_id>/', get_song, name='get-song'),
]