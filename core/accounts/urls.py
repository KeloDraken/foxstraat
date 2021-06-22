from django.urls import path

from core.accounts.views import (
    user_registration, 
    user_login,
)

app_name = 'accounts'

urlpatterns = [
    path('register/', user_registration, name='user-register'),
    path('login/', user_login, name='user-login'),
]