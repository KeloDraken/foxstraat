from django.contrib.auth.decorators import login_required
from django.shortcuts import render

from core.forums.models import Category, Topic


def forum(request):
    return render(request, 'views/topics/topic_list.html')

def get_topic(request, topic_id):
    category = Category.objects.get(object_id=topic_id)
    return render(request, 'views/topics/topic_list.html')