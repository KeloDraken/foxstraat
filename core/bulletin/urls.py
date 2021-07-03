from django.urls import path

from core.bulletin.views import (
    create_bulletin, 
    explore_bulletins,
    get_bulletin,
)


app_name = 'bulletin'

urlpatterns = [
    path('add/', create_bulletin, name='create-bulletin'),
    path('<bulletin_id>/', get_bulletin, name='get-bulletin'),
    path('', explore_bulletins, name='explore-bulletins'),
]