from django.contrib import messages
from django.contrib.auth.decorators import login_required

from django.http.response import Http404
from django.shortcuts import get_object_or_404, redirect, render

from django.shortcuts import render

from utils.helpers import (
    object_id_generator,
    ref_from_url
)

from core.forms import FormWithCaptcha

from core.music.forms import AddSongForm
from core.music.models import Song


@login_required
def add_song(request):
    ref_from_url(request)
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
                        return redirect('bulletin:add-song')
                    
                    spotify = request.POST.get('spotify')
                    soundcloud = request.POST.get('soundcloud')
                    youtube = request.POST.get('youtube')

                    if len(spotify) <= 0 or spotify == None \
                    and len(soundcloud) <= 0 or soundcloud == None \
                    and len(youtube) <= 0 or youtube == None:
                        messages.error(request, 'You need to provide a link to your song')
                        return redirect('bulletin:add-song')
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
                        post_form.save()
                        
                        return redirect(f'/p/songs/{object_id}')

                else:    
                    messages.error(request, 'Post creation failed')
            else:
                messages.error(
                    request, 
                    'Please confirm that you\'re not a robot'
                )
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
    ref_from_url(request)
    post = get_object_or_404(Song, object_id=song_id)

    if request.user.is_authenticated:
        post.upvotes += 1
        post.save()

    more_from_user = Song.objects.filter(
        user=post.user
    ).order_by('?')[:2]

    context = {
        'post': post,
        'more_from_user': more_from_user
    }
    return render(
        request, 
        'views/music/view_song.html', 
        context
    )

def music_chart(request):
    songs = Song.objects.all().order_by('-upvotes')
    context = {
        'songs': songs,
    }
    return render(
        request, 
        'views/music/charts.html', 
        context
    )

def get_genre(request, genre):
    songs = Song.objects.filter(genre__icontains=genre).order_by('-upvotes')
    context = {
        'genre': genre,
        'songs': songs,
    }
    return render(
        request, 
        'views/music/view_genre.html', 
        context
    )