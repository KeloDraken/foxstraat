from django.contrib import admin
from foxstraat.core.models import (
    Feedback,
    ForbiddenWebsites,
    News,
    Privacy,
    Rules,
    Terms,
)


admin.site.register(News)


class ForbiddenWebsitesAdmin(admin.ModelAdmin):
    search_fields = (
        "protocol",
        "host",
        "domain",
    )
    list_display = (
        "parent_domain",
        "host",
        "domain",
    )


admin.site.register(ForbiddenWebsites, ForbiddenWebsitesAdmin)
admin.site.register(Feedback)

# Legal
admin.site.register(Rules)
admin.site.register(Terms)
admin.site.register(Privacy)
