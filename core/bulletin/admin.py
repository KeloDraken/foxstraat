from django.contrib import admin

from core.bulletin.models import (
    Bulletin,
    BulletinImage,
)

class BulletinImageInline(admin.TabularInline):
    model = BulletinImage
    extra = 3

class BulletinAdmin(admin.ModelAdmin):
    inlines = [ BulletinImageInline, ]

admin.site.register(Bulletin, BulletinAdmin)