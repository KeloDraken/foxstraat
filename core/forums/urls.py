from django.urls import path
from core.forums.views import forum

app_name = 'forums'

urlpatterns = [
    path('', forum, name='get-forum'),
]