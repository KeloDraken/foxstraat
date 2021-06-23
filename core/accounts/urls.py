from django.urls import path

from core.accounts.views import (
    user_registration, 
    user_login,
    user_logout,
    user_dashboard,
)

app_name = 'accounts'

urlpatterns = [
    path('register/', user_registration, name='user-register'),
    path('login/', user_login, name='user-login'),
    path("logout/", user_logout, name="user-logout"),

    path('dashboard/', user_dashboard, name='user-dashboard'),
]