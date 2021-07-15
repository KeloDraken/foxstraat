from django.urls import path

from core.bulletin.views import (
    create_bulletin,
    delete_post, 
    explore_bulletins,
    get_bulletin,
    manage_posts
)


app_name = 'bulletin'

urlpatterns = [
    path('add/', create_bulletin, name='create-bulletin'),
    path('manage/', manage_posts, name='manage-posts'),
    path('delete/<bulletin_id>', delete_post, name='delete-post'),

    path('<bulletin_id>/', get_bulletin, name='get-bulletin'),
    path('', explore_bulletins, name='explore-bulletins'),
]