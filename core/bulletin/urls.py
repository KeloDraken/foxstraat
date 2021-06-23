import builtins
from django.urls import path

from core.bulletin.views import create_bulletin

app_name = 'bulletin'

urlpatterns = [
    path('add/', create_bulletin, name='create-bulletin'),
]