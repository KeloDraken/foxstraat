from django.shortcuts import redirect, render

from foxstraat.utils.helpers import is_mobile
from foxstraat.core.bulletin.models import PostTag, Tag


def forum(request):
    if not is_mobile(request):
        return render(request, "views/page_coming_soon.html")
    else:
        return redirect("index")


def get_topic(request, topic_id):
    category = Tag.objects.get(name=topic_id)
    objects = PostTag.objects.filter(tag=category)

    context = {
        "objects": objects,
        "topic_name": topic_id,
    }

    return render(request, "views/topics/view_topic.html", context)
