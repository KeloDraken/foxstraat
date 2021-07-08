from django.urls import path

from core.marketplace.views import storefront

app_name = 'marketplace'

urlpatterns = [
    path('', storefront, name='storefront'),
]