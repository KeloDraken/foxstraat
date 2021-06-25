from django.contrib.auth.decorators import login_required
from django.shortcuts import render, HttpResponse


def forum(request):
    return HttpResponse('HEY!!!')