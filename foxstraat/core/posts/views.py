import calendar
import random
from datetime import date

from django.contrib import messages
from django.contrib.auth.decorators import login_required

from django.core.paginator import Paginator

from django.http.response import Http404, HttpResponseForbidden, JsonResponse
from django.shortcuts import get_object_or_404, redirect, render

from foxstraat.utils.db import cast_vote, check_has_user_voted
from foxstraat.utils.helpers import (
    extract_hashtags,
    is_mobile,
    link_tags_to_post,
    object_id_generator,
)

from foxstraat.core.forms import FormWithCaptcha

from foxstraat.core.posts.forms import CreateBulletinForm
from foxstraat.core.posts.models import Post, Vote


def user_cast_vote(request, bulletin_id):
    if not request.user.is_authenticated:
        return HttpResponseForbidden()
    else:
        bulletin = get_object_or_404(Post, object_id=bulletin_id)

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


def handle_post_save(request, post_form):
    post_form = post_form.save(commit=False)
    post_form.user = request.user

    if request.FILES.get("image"):
        post_form.image = request.FILES.get("image")
    else:
        messages.error(request, "Post wasn't created. No image was found")
        return redirect("bulletin:create-bulletin")

    object_id = object_id_generator(11, Post)
    post_form.object_id = object_id

    caption = request.POST["caption"]

    hashtags = extract_hashtags(text=caption)

    increment_user_num_posts(request)

    post_form.save()

    link_tags_to_post(post_id=object_id, tags=hashtags)
    return redirect("bulletin:get-bulletin", bulletin_id=object_id)


@login_required
def create_bulletin(request):
    captcha = FormWithCaptcha()

    if request.method == "POST":
        post_form = CreateBulletinForm(request.POST)

        has_valid_captcha = check_captcha(request)

        if has_valid_captcha:
            if post_form.is_valid():
                return handle_post_save(request=request, post_form=post_form)

            else:
                messages.error(request, "Post creation failed")
        else:
            messages.error(request, "Please confirm that you're not a robot")
    else:
        post_form = CreateBulletinForm()

    context = {
        "post_form": post_form,
        "captcha": captcha,
    }
    return render(request, "private/posts/create_post.html", context)


def get_bulletin(request, bulletin_id):
    if not is_mobile(request):
        post = get_object_or_404(Post, object_id=bulletin_id)

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
    else:
        return redirect("index")


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
    is_mobile_ = is_mobile(request)
    if not is_mobile_:
        return render(request, "public/posts/frontpage.html", context)
    else:
        return render(request, "mobile/views/frontpage/frontpage.html", context)


@login_required
def manage_posts(request):
    posts = Post.objects.filter(user=request.user).order_by("-datetime_created")
    if not posts:
        messages.error(request, "You don't have any posts yet. Create your post")
        return redirect("bulletin:create-bulletin")
    else:
        context = {"posts": posts}

        return render(request, "private/posts/manage_posts.html", context)


@login_required
def delete_post(request, bulletin_id):
    try:
        bulletin = Post.objects.get(object_id=bulletin_id)
    except:
        raise Http404

    if not bulletin.user == request.user:
        raise Http404

    else:
        bulletin.delete()
        messages.success(request, "Your post has been deleted")
        return redirect("bulletin:manage-posts")
