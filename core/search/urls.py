from django.urls import path

from core.search.views import search


app_name = 'search'
urlpatterns = [
    path('', search, name='search')
]