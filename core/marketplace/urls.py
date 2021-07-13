from django.urls import path

from core.marketplace.views import (
    add_listing, 
    storefront,
    view_listing
)

app_name = 'marketplace'

urlpatterns = [
    path('', storefront, name='storefront'),
    path('new/', add_listing, name='add-listing'),
    path('<listing_id>/', view_listing, name='view-listing'),
]