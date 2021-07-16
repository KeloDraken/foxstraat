from django.urls import path
from core.blog.views import add_blog_post, get_engineering_blog

app_name = 'blog'

urlpatterns = [
    path('add/', add_blog_post, name='add-blog'),
    path('engineering/<blog_id>/', get_engineering_blog, name='get-engineering-blog'),
]