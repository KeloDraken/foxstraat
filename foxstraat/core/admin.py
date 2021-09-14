from django.contrib import admin
from foxstraat.core.models import Feedback, News, Privacy, Rules, Terms


admin.site.register(News)
admin.site.register(Feedback)

# Legal
admin.site.register(Rules)
admin.site.register(Terms)
admin.site.register(Privacy)
