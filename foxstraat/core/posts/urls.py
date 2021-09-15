from django.urls import path

from foxstraat.core.posts.views import (
    create_post,
    delete_post,
    frontpage,
    get_post,
    manage_posts,
    user_cast_vote,
)


app_name = "bulletin"

urlpatterns = [
    path("", frontpage, name="frontpage"),
    path("add/", create_post, name="create-post"),
    path("vote/<post_id>/", user_cast_vote, name="cast-vote"),
    path("manage/", manage_posts, name="manage-posts"),
    path("delete/<post_id>", delete_post, name="delete-post"),
    path("<post_id>/", get_post, name="get-post"),
]
