"""foxstraat URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.views.generic.base import TemplateView
from django.contrib.auth.models import Group

from django.conf import settings
from django.conf.urls.static import static

from django.urls import include, path

from foxstraat.core.accounts.views import (
    get_user_profile,
)

from foxstraat.core.views import about, index, news, privacy, rules, terms

urlpatterns = (
    [
        path("u/admin/", admin.site.urls, name="admin"),
        path("", index, name="index"),
        path("about/", about, name="about"),
        path("news/", news, name="news"),
        path(
            "robots.txt",
            TemplateView.as_view(template_name="robots.txt", content_type="text/plain"),
        ),
        # Legal
        path("privacy/", privacy, name="privacy"),
        path("rules/", rules, name="rules"),
        path("terms/", terms, name="terms"),
        # Accounts urls
        path("u/", include("foxstraat.core.accounts.urls", namespace="accounts")),
        # Bulletin urls
        path("f/", include("foxstraat.core.bulletin.urls", namespace="bulletin")),
        # Search urls
        path("search/", include("foxstraat.core.search.urls", namespace="search")),
        # User main profile
        path("<username>/", get_user_profile, name="get-user-profile"),
    ]
    + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
)

admin.site.site_header = "Foxstraat Site Admin"
admin.site.site_title = "Foxstraat Site Admin"

admin.site.unregister(Group)
