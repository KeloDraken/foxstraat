from django.urls import path

from core.marketplace.views import (
    add_listing, 
    storefront
)

app_name = 'marketplace'

urlpatterns = [
    path('', storefront, name='storefront'),
    path('new/', add_listing, name='add-listing'),
]