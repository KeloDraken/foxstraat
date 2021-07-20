import calendar
from datetime import date
from random import random

from django.core.paginator import Paginator
from django.shortcuts import render

from core.linkoff.models import Link


def get_links(request):
    qs = Link.objects.all().order_by('-datetime_created')
    
    paginator = Paginator(qs, 20)
    
    try:
        page_number = int(request.GET.get('sida'))
    except:
        page_number = 1
    
    page_obj = paginator.get_page(page_number)

    current_date = date.today()
    weekday = calendar.day_name[current_date.weekday()]
    score = round(random.randint(-1000,1000)/55)
    context = {
        'score': score,
        'heading': f'Foxstraat Linkoff',
        'page_obj': page_obj
    }
    
    return render(
        request, 
        'views/linkoff/get_links.html',
        context
    )
