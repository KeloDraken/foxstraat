from django.contrib import admin

from core.bulletin.models import (
    Bulletin,
    Tag,
    Vote,
)


class BulletinAdmin(admin.ModelAdmin):
    search_fields = (
        'object_id',
    )

admin.site.register(Bulletin, BulletinAdmin)
admin.site.register(Vote)
admin.site.register(Tag)