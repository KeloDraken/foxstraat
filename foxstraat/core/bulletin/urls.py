from django.urls import path

from foxstraat.core.bulletin.views import (
    create_bulletin,
    delete_post,
    frontpage,
    get_bulletin,
    manage_posts,
    user_cast_vote,
)


app_name = "bulletin"

urlpatterns = [
    path("", frontpage, name="frontpage"),
    path("photo/<bulletin_id>/", get_bulletin, name="get-bulletin"),
    path("add/", create_bulletin, name="create-bulletin"),
    path("vote/<bulletin_id>/", user_cast_vote, name="cast-vote"),
    path("manage/", manage_posts, name="manage-posts"),
    path("delete/<bulletin_id>", delete_post, name="delete-post"),
]