from django.urls import path
from core.linkoff.views import get_links

app_name = 'linkoff'

urlpatterns = [
    path('', get_links, name='get-links')
]