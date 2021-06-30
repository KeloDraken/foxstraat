from django.contrib import admin

from core.bulletin.models import (
    Bulletin,
    BulletinImage,
    Tag,
)

class BulletinImageInline(admin.TabularInline):
    model = BulletinImage
    extra = 3

class BulletinAdmin(admin.ModelAdmin):
    inlines = [ BulletinImageInline, ]

admin.site.register(Bulletin, BulletinAdmin)
admin.site.register(Tag)