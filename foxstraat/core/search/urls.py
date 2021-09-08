from django.urls import path

from foxstraat.core.search.views import search


app_name = "search"
urlpatterns = [path("", search, name="search")]
