from django.urls import path
from foxstraat.core.forums.views import forum, get_topic

app_name = "forums"

urlpatterns = [
    path("", forum, name="get-forum"),
    path("<topic_id>/", get_topic, name="get-topic"),
]
