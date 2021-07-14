from django.contrib import admin

from core.bulletin.models import (
    Bulletin,
    Song,
    Tag,
)


admin.site.register(Bulletin)
admin.site.register(Tag)
admin.site.register(Song)