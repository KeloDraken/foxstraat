from django.urls import path

from core.bulletin.views import (
    create_bulletin,
    delete_post,
    explore_photos, 
    frontpage,
    get_bulletin,
    manage_posts
)


app_name = 'bulletin'

urlpatterns = [
    path('', frontpage, name='explore-bulletins'),
    path('photo/', explore_photos, name='explore-photos'),
    path('photo/<bulletin_id>/', get_bulletin, name='get-bulletin'),


    path('add/', create_bulletin, name='create-bulletin'),
    path('manage/', manage_posts, name='manage-posts'),
    path('delete/<bulletin_id>', delete_post, name='delete-post'),

]