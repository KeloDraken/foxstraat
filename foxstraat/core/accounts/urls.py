from django.urls import path

from foxstraat.core.accounts.views import (
    delete_account,
    explore_users,
    user_registration,
    user_login,
    user_logout,
    edit_user_profile,
)

app_name = "accounts"

urlpatterns = [
    path("register/", user_registration, name="user-register"),
    path("login/", user_login, name="user-login"),
    path("logout/", user_logout, name="user-logout"),
    path("edit/", edit_user_profile, name="edit-user-profile"),
    path("explore/", explore_users, name="explore-users"),
    path("delete/", delete_account, name="delete-user"),
]
