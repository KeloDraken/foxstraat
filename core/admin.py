from django.contrib import admin
from core.models import Ref, Feedback, News


class RefAdmin(admin.ModelAdmin):
    list_display = (
        'source',
        'hits',
    )

admin.site.register(Ref, RefAdmin)
admin.site.register(News)
admin.site.register(Feedback)