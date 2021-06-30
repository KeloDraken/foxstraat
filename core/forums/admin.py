from django.contrib import admin

from core.forums.models import Category, Topic


admin.site.register(Category)
admin.site.register(Topic)