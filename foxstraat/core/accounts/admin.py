from django.contrib import admin

from foxstraat.core.accounts.models import User


class UserAdmin(admin.ModelAdmin):
    search_fields = ("email",)
    list_display = (
        "email",
        "date_joined",
    )


admin.site.register(User, UserAdmin)
