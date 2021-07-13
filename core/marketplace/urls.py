from django.urls import path

from core.marketplace.views import (
    add_listing,
    buy_template,
    delete_listing,
    manage_listings, 
    storefront,
    view_listing
)

app_name = 'marketplace'

urlpatterns = [
    path('', storefront, name='storefront'),
    path('new/', add_listing, name='add-listing'),
    path('manage/', manage_listings, name='manage-listing'),
    path('delete/<listing_id>/', delete_listing, name='delete-listing'),
    path('buy/<listing_id>/', buy_template, name='buy-template'),
    path('<listing_id>/', view_listing, name='view-listing'),
]