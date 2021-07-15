from django.urls import path
from core.blog.views import get_blog

app_name = 'blog'

urlpatterns = [
    path('<blog_id>/', get_blog, name='get-blog'),
]