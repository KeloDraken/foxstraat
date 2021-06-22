from django.urls import path

from core.accounts.views import user_registration

app_name = 'accounts'

urlpatterns = [
    path('register/', user_registration, name='user-register'),
]