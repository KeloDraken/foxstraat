from django.contrib.auth.decorators import login_required
from django.shortcuts import render, HttpResponse


def forum(request):
    return render(request, 'views/page_coming_soon.html')