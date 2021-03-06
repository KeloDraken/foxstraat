from foxstraat.utils.db import fetch_porn_sites_json
from django.contrib import messages
from django.shortcuts import redirect, render

from foxstraat.utils.helpers import object_id_generator
from foxstraat.core.models import Feedback, News, Privacy, Rules, Terms


def add_feedback(request):
    if request.method == "POST":
        feedback = request.POST.get("feedback")

        if not len(feedback) <= 0 and not feedback == None:
            object_id = object_id_generator(11, Feedback)
            Feedback.objects.create(object_id=object_id, body=feedback)

            messages.success(
                request, "Thank you for the feedback. We will review it soon"
            )
            return redirect("about")

        else:
            messages.error(
                request, "Something went wrong. We couldn't send your feedback"
            )
            return redirect("about")


def dump_sites(request):
    return fetch_porn_sites_json()


def index(request):
    return render(request, "public/index.html")


def news(request):
    news_ = News.objects.all().order_by("-datetime_created")
    context = {"heading": "Foxstraat News", "news": news_}
    return render(request, "views/blog/news.html", context)


def about(request):
    add_feedback(request)
    return render(request, "views/index.html", context={"page": "about"})


def terms(request):
    news_ = Terms.objects.all()
    context = {"heading": "Terms of Service", "news": news_}
    return render(request, "views/blog/news.html", context)


def privacy(request):
    news_ = Privacy.objects.all()
    context = {"heading": "Privacy Policy", "news": news_}
    return render(request, "views/blog/news.html", context)


def rules(request):
    news_ = Rules.objects.all()
    context = {"heading": "Foxstraat Rules", "news": news_}
    return render(request, "views/blog/news.html", context)
