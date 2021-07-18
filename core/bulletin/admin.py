from django.contrib import admin

from core.bulletin.models import (
    Bulletin,
    Tag,
    Vote,
)


admin.site.register(Bulletin)
admin.site.register(Vote)
admin.site.register(Tag)