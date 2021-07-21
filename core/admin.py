from django.contrib import admin
from core.models import (
    Feedback, 
    News, 
    Privacy, 
    Ref, 
    Rules, 
    Terms
)


class RefAdmin(admin.ModelAdmin):
    list_display = (
        'source',
        'hits',
    )

admin.site.register(Ref, RefAdmin)
admin.site.register(News)
admin.site.register(Feedback)

# Legal
admin.site.register(Rules)
admin.site.register(Terms)
admin.site.register(Privacy)