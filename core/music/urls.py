from django.urls import path

from core.music.views import (
    add_song,
    alltime_music_chart,
    delete_song, 
    get_genre, 
    get_song,
    hot_music_chart,
    manage_songs,
    new_music_chart, 
    top_music_chart
)

app_name = 'music'

urlpatterns = [
    # Music
    path('top/', top_music_chart, name='explore-music'),
    path('new/', new_music_chart, name='new-music'),
    path('hot/', hot_music_chart, name='hot-music'),
    path('all/', alltime_music_chart, name='all-time-music'),
    path('add/', add_song, name='add-song'),
    path('genre/<genre>/', get_genre, name='get-genre'),
    path('manage/', manage_songs, name='manage-songs'),
    path('delete/<song_id>/', delete_song, name='delete-song'),
    path('<song_id>/', get_song, name='get-song'),
]