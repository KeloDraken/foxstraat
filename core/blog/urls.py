from django.urls import path
from core.blog.views import add_blog_post, get_blog

app_name = 'blog'

urlpatterns = [
    path('add/', add_blog_post, name='add-blog'),
    path('<blog_id>/', get_blog, name='get-blog'),
]