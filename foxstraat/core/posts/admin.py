from django.contrib import admin

from foxstraat.core.posts.models import (
    Post,
    Vote,
)


class PostAdmin(admin.ModelAdmin):
    search_fields = ("object_id",)


admin.site.register(Post, PostAdmin)
admin.site.register(Vote)
