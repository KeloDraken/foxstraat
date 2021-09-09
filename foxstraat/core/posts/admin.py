from django.contrib import admin

from foxstraat.core.posts.models import (
    Post,
    Tag,
    Vote,
)


class BulletinAdmin(admin.ModelAdmin):
    search_fields = ("object_id",)


admin.site.register(Post, BulletinAdmin)
admin.site.register(Vote)
admin.site.register(Tag)
