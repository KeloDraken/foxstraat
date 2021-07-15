from django.urls import path

from core.bulletin.views import (
    add_song,
    create_bulletin,
    delete_post, 
    explore_bulletins,
    get_bulletin,
    get_song,
    manage_posts,
    music_chart,
)


app_name = 'bulletin'

urlpatterns = [
    path('add/', create_bulletin, name='create-bulletin'),
    path('manage/', manage_posts, name='manage-posts'),
    path('delete/<bulletin_id>', delete_post, name='delete-post'),

    # Music
    path('songs/add/', add_song, name='add-song'),
    path('songs/explore/', music_chart, name='explore-music'),
    path('songs/<song_id>/', get_song, name='get-song'),
    
    path('<bulletin_id>/', get_bulletin, name='get-bulletin'),
    path('', explore_bulletins, name='explore-bulletins'),
]