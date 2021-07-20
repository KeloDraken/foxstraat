from django.urls import path
from core.announcements.views import (
    create_announcement, 
    create_product_announcement
)

app_name = 'announcements'

urlpatterns = [
    path('create/', create_announcement, name='create-announcement'),
    path('create/product/', create_product_announcement, name='create-product-announcement'),
]