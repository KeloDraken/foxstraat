import calendar
from datetime import date

from django.contrib import messages
from django.contrib.auth.decorators import login_required

from django.core.paginator import Paginator
from django.http.response import HttpResponseBadRequest, HttpResponseForbidden

from django.shortcuts import get_object_or_404, redirect, render

from utils.helpers import object_id_generator

from core.forms import FormWithCaptcha

from core.music.forms import AddSongForm
from core.music.models import Song


@login_required
def add_song(request):
    if not request.user.is_artist:
        messages.error(request, 'You\'re not an artist yet. Go to Edit profile to convert your account')
        return redirect('index')
    else:
        captcha = FormWithCaptcha()

        if request.method == 'POST':   
            post_form = AddSongForm(request.POST)
            # TODO: remove this try/catch in production
            try:
                captcha_data = request.POST['g-recaptcha-response']
            except:
                captcha_data = '...'
                
            if not captcha_data == '':
                
                if post_form.is_valid():
                    post_form = post_form.save(commit=False)
                    post_form.user = request.user

                    if request.FILES.get('cover_art'):
                        post_form.cover_art = request.FILES.get('cover_art')
                    else:
                        messages.error(request, 'Song wasn\'t added. No cover art was found')
                        return redirect('music:add-song')
                    
                    spotify = request.POST.get('spotify')
                    soundcloud = request.POST.get('soundcloud')
                    youtube = request.POST.get('youtube')

                    if len(spotify) <= 0 or spotify == None:
                        spotify = None
                    else:
                        spotify = spotify
                        
                    if len(soundcloud)<=0 or soundcloud == None:
                        soundcloud = None
                    else:
                        soundcloud = soundcloud

                    if len(youtube)<=0 or youtube == None:
                        youtube = None
                    else:
                        youtube = youtube

                    if spotify == None and soundcloud == None and youtube == None:
                        messages.error(request, 'You need to provide a link to your song')
                        return redirect('music:add-song')
                        
                    else:
                        object_id = object_id_generator(11, Song)
                        post_form.object_id = object_id
                        
                        is_explicit = request.POST.get('is_explicit')
                        if is_explicit == 'on':
                            post_form.is_explicit = True
                        else:
                            pass

                        artists = request.POST.get('artists')
                        if not len(artists) <= 0 and not artists == None:
                            post_form.artists = artists
                        else:
                            post_form.artists = request.user.display_name
                        

                        request.user.num_posts =+ 1
                        request.user.save()
                        
                        post_form.spotify = spotify
                        post_form.soundcloud = soundcloud
                        post_form.youtube = youtube

                        post_form.save()
                        
                        return redirect('music:get-song', song_id=object_id)

                else:    
                    messages.error(request, 'Something went wrong. We couldn\'t add you song. Please try again')
                    return redirect('music:add-song')
            else:
                messages.error(
                    request, 
                    'Please confirm that you\'re not a robot'
                )
                return redirect('music:add-song')
        else:
            post_form = AddSongForm()

        context = {
            'post_form': post_form,
            'captcha': captcha,
        }
        return render(
            request, 
            'views/music/add_song.html', 
            context
        )

def get_song(request, song_id):
    post = get_object_or_404(Song, object_id=song_id)

    if request.user.is_authenticated:
        post.upvotes += 1
        post.save()

    more_from_user = Song.objects.filter(
        user=post.user
    ).order_by('?')[:4]

    context = {
        'post': post,
        'more_from_user': more_from_user
    }
    return render(
        request, 
        'views/music/view_song.html', 
        context
    )

def top_music_chart(request):
    songs = Song.objects.all().order_by('-upvotes')
    paginator = Paginator(songs, 10)

    try:
        page_number = int(request.GET.get('sida'))
    except:
        page_number = 1

    page_obj = paginator.get_page(page_number)
    
    current_date = date.today()
    weekday = calendar.day_name[current_date.weekday()]

    context = {
        'page_obj': page_obj,
        'heading': f'Foxstraat {weekday} Hot 100',
    }
    return render(
        request, 
        'views/music/charts.html', 
        context
    )

def new_music_chart(request):
    songs = Song.objects.all().order_by('-datetime_created')
    paginator = Paginator(songs, 10)
    
    try:
        page_number = int(request.GET.get('sida'))
    except:
        page_number = 1

    page_obj = paginator.get_page(page_number)

    if page_number > 1:
        add_10 = True
    else:
        add_10 = False
    
    context = {
        'add_10': add_10,
        'page_obj': page_obj,
        'heading': 'Recent submissions',
    }
    return render(
        request, 
        'views/music/charts.html', 
        context
    )

def hot_music_chart(request):
    songs = Song.objects.all().order_by('-upvotes')
    paginator = Paginator(songs, 10)
    
    try:
        page_number = int(request.GET.get('sida'))
    except:
        page_number = 1

    page_obj = paginator.get_page(page_number)


    context = {
        'page_obj': page_obj,
        'heading': 'Trending today',
    }
    return render(
        request, 
        'views/music/charts.html', 
        context
    )

def alltime_music_chart(request):
    songs = Song.objects.all().order_by('-upvotes')
    paginator = Paginator(songs, 10)
    
    try:
        page_number = int(request.GET.get('sida'))
    except:
        page_number = 1

    page_obj = paginator.get_page(page_number)

    context = {
        'page_obj': page_obj,
        'heading': f'All time top voted',
    }
    return render(
        request, 
        'views/music/charts.html', 
        context
    )

def get_genre(request, genre):
    songs = Song.objects.filter(genre__icontains=genre).order_by('-upvotes')
    paginator = Paginator(songs, 10)
    
    try:
        page_number = int(request.GET.get('sida'))
    except:
        page_number = 1

    page_obj = paginator.get_page(page_number)

    context = {
        'genre': genre,
        'page_obj': page_obj,
    }
    return render(
        request, 
        'views/music/view_genre.html', 
        context
    )

@login_required
def manage_songs(request):
    posts = Song.objects.filter(user=request.user).order_by('-datetime_created')
    if not posts:
        messages.error(request, 'You don\'t have any songs yet. Add your first song')
        return redirect('music:add-song')
    else:
        context = {
            'posts': posts
        }
        
        return render(
            request, 
            'views/music/manage_songs.html',
            context
        )

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
        messages.success(request, 'Your song has been deleted')
        return redirect('music:manage-songs')