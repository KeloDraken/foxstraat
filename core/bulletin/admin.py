from django.contrib import admin

from core.bulletin.models import (
    Bulletin,
    Tag,
)


admin.site.register(Bulletin)
admin.site.register(Tag)