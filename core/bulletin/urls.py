import builtins
from django.urls import path

from core.bulletin.views import (
    create_bulletin, 
    explore_bulletins
)


app_name = 'bulletin'

urlpatterns = [
    path('add/', create_bulletin, name='create-bulletin'),
    path('', explore_bulletins, name='explore-bulletins'),
]