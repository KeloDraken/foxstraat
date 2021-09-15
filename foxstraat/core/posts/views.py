import calendar
from datetime import date
import random

from django.contrib import messages
from django.contrib.auth.decorators import login_required

from django.core.exceptions import ValidationError
from django.core.paginator import Paginator

from django.forms import URLField
from django.http.response import (
    Http404,
    HttpResponse,
    HttpResponseForbidden,
    JsonResponse,
)
from django.shortcuts import get_object_or_404, redirect, render

from foxstraat.utils.db import cast_vote, check_has_user_voted
from foxstraat.utils.helpers import extract_page_data, is_forbidden, object_id_generator

from foxstraat.core.forms import FormWithCaptcha

from foxstraat.core.posts.forms import CreatePostForm
from foxstraat.core.posts.models import Post, Vote


def user_cast_vote(request, post_id):
    if not request.user.is_authenticated:
        return HttpResponseForbidden()
    else:
        bulletin = get_object_or_404(Post, object_id=post_id)

        try:
            vote_value = int(request.GET.get("vote_value"))
        except:
            vote_value = 0

        has_user_voted = check_has_user_voted(Vote, request.user, bulletin)

        if has_user_voted == True:
            vote = Vote.objects.get(user=request.user, bulletin=bulletin)
            if vote.value == -1 or vote.value == 1:
                cast_vote(bulletin=bulletin, vote_value=0, vote=vote)
            elif vote.value == 0:
                cast_vote(bulletin=bulletin, vote_value=vote_value, vote=vote)

            return JsonResponse({"score": bulletin.score, "has_voted": True})
        elif has_user_voted == False:
            vote = Vote.objects.create(user=request.user, bulletin=bulletin)
            cast_vote(bulletin, vote_value, vote)
            return JsonResponse(data={"score": bulletin.score, "has_voted": True})


def check_captcha(request):
    """
    Checks if request object has valid captcha
    """
    captcha_data = request.POST["g-recaptcha-response"]
    if not captcha_data == "" and not captcha_data == None:
        return True
    return False


def increment_user_num_posts(request):
    request.user.num_posts = request.user.num_posts + 1
    request.user.save()


def validate_url(url):
    url_form_field = URLField()
    try:
        url = url_form_field.clean(url)
    except ValidationError:
        return False
    return True


@login_required
def create_post(request):
    if not request.method == "POST":
        context = {
            "captcha": FormWithCaptcha,
            "is_auth_page": True,
        }
        return render(request, "private/submit_link.html", context)
    else:
        url = request.POST.get("page_link")
        # captcha_data = request.POST.get("g-recaptcha-response")

        if not url == None and not url == "":
            is_url_valid = validate_url(url)

            if is_url_valid:
                is_forbidden_url = is_forbidden(url=url)
                if is_forbidden_url == False:
                    return extract_page_data(url=url, request=request)
                else:
                    messages.error(
                        request,
                        "Link wasn't added because the host is banned from Foxstraat",
                    )
                    return redirect("posts:create-post")
            else:
                messages.error(request, "Invalid url")
                return redirect("posts:create-post")
        else:
            messages.error(request, "No link found")
            return redirect("posts:create-post")


def get_post(request, post_id):
    post = get_object_or_404(Post, object_id=post_id)

    more_from_user = Post.objects.filter(user=post.user).order_by("?")[:4]

    has_voted = False
    has_downvoted = False
    has_upvoted = False

    if request.user.is_authenticated:
        has_voted = check_has_user_voted(Vote, request.user, post)

        if has_voted:
            vote = Vote.objects.get(user=request.user, bulletin=post)
            if vote.value == -1:
                has_downvoted = True
                has_upvoted = False
            elif vote.value == 1:
                has_downvoted = False
                has_upvoted = True
            else:
                has_downvoted = False
                has_upvoted = False

    upvotes = round(post.upvotes - post.downvotes)
    context = {
        "has_upvoted": has_upvoted,
        "has_downvoted": has_downvoted,
        "post": post,
        "upvotes": upvotes,
        "more_from_user": more_from_user,
    }
    return render(request, "public/posts/view_post.html", context)


def frontpage(request):
    qs = Post.objects.all().order_by("-datetime_created")

    paginator = Paginator(qs, 20)

    try:
        page_number = int(request.GET.get("sida"))
    except:
        page_number = 1

    page_obj = paginator.get_page(page_number)

    current_date = date.today()
    weekday = calendar.day_name[current_date.weekday()]
    score = round(random.randint(-1000, 1000) / 55)
    context = {
        "score": score,
        "heading": f"Explore {weekday}'s photos",
        "page_obj": page_obj,
    }
    return render(request, "public/posts/frontpage.html", context)


@login_required
def manage_posts(request):
    posts = Post.objects.filter(user=request.user).order_by("-datetime_created")
    if not posts:
        messages.error(request, "You don't have any posts yet. Create your post")
        return redirect("posts:create-post")
    else:
        context = {"posts": posts}

        return render(request, "private/posts/manage_posts.html", context)


@login_required
def delete_post(request, post_id):
    try:
        post = Post.objects.get(object_id=post_id)
    except:
        raise Http404

    if not post.user == request.user:
        raise Http404

    else:
        post.delete()
        messages.success(request, "Your post has been deleted")
        return redirect("posts:manage-posts")
