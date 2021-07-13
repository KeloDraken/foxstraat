from django.urls import path

from core.marketplace.views import (
    add_listing,
    buy_template, 
    storefront,
    view_listing
)

app_name = 'marketplace'

urlpatterns = [
    path('', storefront, name='storefront'),
    path('new/', add_listing, name='add-listing'),
    path('buy/<listing_id>/', buy_template, name='buy-template'),
    path('<listing_id>/', view_listing, name='view-listing'),
]