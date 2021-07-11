from django.shortcuts import render

from utils.helpers import ref_from_url

from core.bulletin.models import PostTag, Tag


def forum(request):
    ref_from_url(request)
    return render(request, 'views/page_coming_soon.html')

def get_topic(request, topic_id):
    ref_from_url(request)
    category = Tag.objects.get(name=topic_id)
    objects = PostTag.objects.filter(tag=category)

    context = {
        'objects': objects,
        'topic_name': topic_id,
    } 

    return render(request, 'views/topics/view_topic.html', context)