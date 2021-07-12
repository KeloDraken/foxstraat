from django.contrib import admin
from core.models import Ref


class RefAdmin(admin.ModelAdmin):
    list_display = (
        'source',
        'hits',
    )

admin.site.register(Ref, RefAdmin)