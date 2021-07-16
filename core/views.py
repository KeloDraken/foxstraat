from django.shortcuts import redirect, render

from utils.helpers import ref_from_url
from core.blog.models import News


def index(request):
    ref_from_url(request)
    if request.user.is_authenticated:
        return redirect('accounts:user-dashboard')
    else:
        return render(request, 'views/index.html')

def news(request):
    news_ = News.objects.all().order_by('-datetime_created')
    context = {
        'news': news_
    }
    return render(request, 'views/blog/news.html', context)

def about(request):
    ref_from_url(request)
    return render(request, 'views/index.html')
