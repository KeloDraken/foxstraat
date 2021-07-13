from django.urls import path

from core.bulletin.views import (
    create_bulletin, 
    explore_bulletins,
    get_bulletin,
    manage_posts,
)


app_name = 'bulletin'

urlpatterns = [
    path('add/', create_bulletin, name='create-bulletin'),
    path('manage/', manage_posts, name='manage-posts'),
    path('<bulletin_id>/', get_bulletin, name='get-bulletin'),
    path('', explore_bulletins, name='explore-bulletins'),
]