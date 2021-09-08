import calendar
from datetime import date
import random

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.http.response import (
    HttpResponseBadRequest,
    HttpResponseForbidden,
    JsonResponse,
)

from django.shortcuts import get_object_or_404, redirect, render

from foxstraat.utils.db import cast_vote, check_has_user_voted
from foxstraat.utils.helpers import is_mobile, object_id_generator

from foxstraat.core.forms import FormWithCaptcha
from foxstraat.core.music.forms import AddSongForm
from foxstraat.core.music.models import Song, VoteSong


def user_cast_vote(request, song_id):
    if not request.user.is_authenticated:
        return HttpResponseForbidden()
    else:
        bulletin = get_object_or_404(Song, object_id=song_id)

        try:
            vote_value = int(request.GET.get("vote_value"))
        except:
            vote_value = 0

        has_user_voted = check_has_user_voted(VoteSong, request.user, bulletin)

        if has_user_voted == True:
            vote = VoteSong.objects.get(user=request.user, bulletin=bulletin)
            if vote.value == -1 or vote.value == 1:
                cast_vote(bulletin=bulletin, vote_value=0, vote=vote)
            elif vote.value == 0:
                cast_vote(bulletin=bulletin, vote_value=vote_value, vote=vote)

            return JsonResponse({"score": bulletin.score, "has_voted": True})
        elif has_user_voted == False:
            vote = VoteSong.objects.create(user=request.user, bulletin=bulletin)
            cast_vote(bulletin, vote_value, vote)
            return JsonResponse(data={"score": bulletin.score, "has_voted": True})


@login_required
def add_song(request):
    if not request.user.is_artist:
        messages.error(
            request,
            "You're not an artist yet. Go to Edit profile to convert your account",
        )
        return redirect("index")
    else:
        captcha = FormWithCaptcha()

        if request.method == "POST":
            post_form = AddSongForm(request.POST)
            # TODO: remove this try/catch in production
            # try:
            captcha_data = request.POST["g-recaptcha-response"]
            # except:
            #     captcha_data = '...'

            if not captcha_data == "" and not captcha_data == None:

                if post_form.is_valid():
                    post_form = post_form.save(commit=False)
                    post_form.user = request.user

                    if request.FILES.get("cover_art"):
                        post_form.cover_art = request.FILES.get("cover_art")
                    else:
                        messages.error(
                            request, "Song wasn't added. No cover art was found"
                        )
                        return redirect("music:add-song")

                    spotify = request.POST.get("spotify")
                    soundcloud = request.POST.get("soundcloud")
                    youtube = request.POST.get("youtube")

                    if len(spotify) <= 0 or spotify == None:
                        spotify = None
                    else:
                        spotify = spotify

                    if len(soundcloud) <= 0 or soundcloud == None:
                        soundcloud = None
                    else:
                        soundcloud = soundcloud

                    if len(youtube) <= 0 or youtube == None:
                        youtube = None
                    else:
                        youtube = youtube

                    if spotify == None and soundcloud == None and youtube == None:
                        messages.error(
                            request, "You need to provide a link to your song"
                        )
                        return redirect("music:add-song")

                    else:
                        object_id = object_id_generator(11, Song)
                        post_form.object_id = object_id

                        is_explicit = request.POST.get("is_explicit")
                        if is_explicit == "on":
                            post_form.is_explicit = True
                        else:
                            pass

                        artists = request.POST.get("artists")
                        if not len(artists) <= 0 and not artists == None:
                            post_form.artists = artists
                        else:
                            post_form.artists = request.user.display_name

                        request.user.num_posts = +1
                        request.user.save()

                        post_form.spotify = spotify
                        post_form.soundcloud = soundcloud
                        post_form.youtube = youtube

                        post_form.save()

                        return redirect("music:get-song", song_id=object_id)

                else:
                    messages.error(
                        request,
                        "Something went wrong. We couldn't add you song. Please try again",
                    )
                    return redirect("music:add-song")
            else:
                messages.error(request, "Please confirm that you're not a robot")
                return redirect("music:add-song")
        else:
            post_form = AddSongForm()

        context = {
            "post_form": post_form,
            "captcha": captcha,
        }
        return render(request, "views/music/add_song.html", context)


def get_song(request, song_id):
    if not is_mobile(request):
        post = get_object_or_404(Song, object_id=song_id)

        more_from_user = Song.objects.filter(user=post.user).order_by("?")[:4]

        has_voted = False
        has_downvoted = False
        has_upvoted = False

        if request.user.is_authenticated:
            has_voted = check_has_user_voted(VoteSong, request.user, post)

            if has_voted:
                vote = VoteSong.objects.get(user=request.user, bulletin=post)
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
            "page": "song",
            "upvotes": upvotes,
            "more_from_user": more_from_user,
        }
        return render(request, "views/music/view_song.html", context)
    else:
        return redirect("index")


def top_music_chart(request):
    qs = Song.objects.all().order_by("-score")

    paginator = Paginator(qs, 10)

    try:
        page_number = int(request.GET.get("sida"))
    except:
        page_number = 1

    page_obj = paginator.get_page(page_number)

    current_date = date.today()
    weekday = calendar.day_name[current_date.weekday()]

    context = {
        "page_obj": page_obj,
        "page": "top",
        "heading": f"Foxstraat {weekday} chart",
    }
    is_mobile_ = is_mobile(request)

    if not is_mobile_:
        return render(request, "views/music/charts.html", context)
    else:
        return render(request, "mobile/views/music/charts.html", context)


def new_music_chart(request):
    songs = Song.objects.all().order_by("-datetime_created")
    paginator = Paginator(songs, 10)

    try:
        page_number = int(request.GET.get("sida"))
    except:
        page_number = 1

    page_obj = paginator.get_page(page_number)

    if page_number > 1:
        add_10 = True
    else:
        add_10 = False

    context = {
        "page": "new",
        "add_10": add_10,
        "page_obj": page_obj,
        "heading": "Recent submissions",
    }
    is_mobile_ = is_mobile(request)

    if not is_mobile_:
        return render(request, "views/music/charts.html", context)
    else:
        return render(request, "mobile/views/music/charts.html", context)


def hot_music_chart(request):
    songs = Song.objects.all().order_by("-datetime_created")

    paginator = Paginator(songs, 10)

    try:
        page_number = int(request.GET.get("sida"))
    except:
        page_number = 1

    page_obj = paginator.get_page(page_number)

    context = {
        "page_obj": page_obj,
        "heading": "Trending today",
    }
    is_mobile_ = is_mobile(request)

    if not is_mobile_:
        return render(request, "views/music/charts.html", context)
    else:
        return render(request, "mobile/views/music/charts.html", context)


def alltime_music_chart(request):
    songs = Song.objects.all().order_by("-upvotes")
    paginator = Paginator(songs, 10)

    try:
        page_number = int(request.GET.get("sida"))
    except:
        page_number = 1

    page_obj = paginator.get_page(page_number)

    context = {
        "page_obj": page_obj,
        "heading": f"All time top voted",
    }
    is_mobile_ = is_mobile(request)

    if not is_mobile_:
        return render(request, "views/music/charts.html", context)
    else:
        return render(request, "mobile/views/music/charts.html", context)


def get_genre(request, genre):
    if not is_mobile(request):
        songs = Song.objects.filter(genre__icontains=genre).order_by("-score")
        paginator = Paginator(songs, 10)

        try:
            page_number = int(request.GET.get("sida"))
        except:
            page_number = 1

        page_obj = paginator.get_page(page_number)

        context = {
            "genre": genre,
            "page_obj": page_obj,
        }
        return render(request, "views/music/view_genre.html", context)
    else:
        return redirect("index")


@login_required
def manage_songs(request):
    posts = Song.objects.filter(user=request.user).order_by("-datetime_created")

    if request.user.is_artist:
        if not posts:
            messages.error(request, "You don't have any songs yet. Add your first song")
            return redirect("music:add-song")
        else:
            context = {"posts": posts}

            return render(request, "views/music/manage_songs.html", context)
    else:
        return redirect("music:add-song")


@login_required
def delete_song(request, song_id):
    try:
        bulletin = Song.objects.get(object_id=song_id)
    except:
        return HttpResponseBadRequest()

    if not bulletin.user == request.user:
        raise HttpResponseForbidden()

    else:
        bulletin.delete()
        messages.success(request, "Your song has been deleted")
        return redirect("music:manage-songs")
