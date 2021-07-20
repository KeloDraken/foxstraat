from django.contrib import admin
from core.announcements.models import Announcement, ProductAnnouncement


admin.site.register(Announcement)
admin.site.register(ProductAnnouncement)