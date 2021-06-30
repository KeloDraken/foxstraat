from django.contrib.auth.decorators import login_required
from django.shortcuts import render


def forum(request):
    return render(request, 'views/page_coming_soon.html')

def get_topic(request, topic_id):
    category = topic_id
    return render(request, 'views/topics/topic_list.html')