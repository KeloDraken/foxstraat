from django.contrib import messages
from django.contrib.auth.decorators import login_required

from django.http.response import Http404
from django.shortcuts import get_object_or_404, redirect, render

from utils.helpers import (
    extract_hashtags,
    link_tags_to_post, 
    object_id_generator,
    ref_from_url
)

from core.forms import FormWithCaptcha

from core.bulletin.forms import (
    AddSongForm,
    CreateBulletinForm
)
from core.bulletin.models import (
    Bulletin,
    Song, 
    Tag
)


@login_required
def create_bulletin(request):
    ref_from_url(request)
    captcha = FormWithCaptcha()

    if request.method == 'POST':        
        post_form = CreateBulletinForm(request.POST)
        # TODO: remove this try/catch in production
        try:
            captcha_data = request.POST['g-recaptcha-response']
        except:
            captcha_data = '...'
            
        if not captcha_data == '':
            if post_form.is_valid():
                post_form = post_form.save(commit=False)
                post_form.user = request.user

                if request.FILES.get('image'):
                    post_form.image = request.FILES.get('image')
                else:
                    messages.error(request, 'Post wasn\'t created. No image was found')
                    return redirect('bulletin:create-bulletin')

                object_id = object_id_generator(11, Bulletin)
                post_form.object_id = object_id
                
                caption = request.POST['caption']
                
                hashtags = extract_hashtags(text=caption)

                request.user.num_posts =+ 1
                request.user.save()
                post_form.save()

                link_tags_to_post(post_id=object_id, tags=hashtags)
                
                return redirect(f'/p/{object_id}')

            else:    
                messages.error(request, 'Post creation failed')
        else:
            messages.error(
                request, 
                'Please confirm that you\'re not a robot'
            )
    else:
        post_form = CreateBulletinForm()

    context = {
        'post_form': post_form,
        'captcha': captcha,
    }
    return render(
        request, 
        'views/bulletin/create_bulletin.html', 
        context
    )

@login_required
def add_song(request):
    ref_from_url(request)
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
                    
                    request.user.num_posts =+ 1
                    request.user.save()
                    post_form.save()
                    
                    return redirect(f'/p/song/{object_id}')

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
        'views/bulletin/add_song.html', 
        context
    )


def get_bulletin(request, bulletin_id):
    ref_from_url(request)
    post = get_object_or_404(Bulletin, object_id=bulletin_id)

    if request.user.is_authenticated:
        post.upvotes += 1
        post.save()

    more_from_user = Bulletin.objects.filter(
        user=post.user
    ).order_by('?')[:2]

    context = {
        'post': post,
        'more_from_user': more_from_user
    }
    return render(
        request, 
        'views/bulletin/view_bulletin.html', 
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
        'views/bulletin/view_song.html', 
        context
    )

def explore_bulletins(request):
    ref_from_url(request)
    posts = Bulletin.objects.all().order_by('-upvotes')

    topics = Tag.objects.all().order_by('?')[:30]
    context = {
        'topics': topics,
        'posts': posts
    }
    
    return render(
        request, 
        'views/bulletin/explore_bulletins.html',
        context
    )

@login_required
def manage_posts(request):
    ref_from_url(request)
    posts = Bulletin.objects.filter(user=request.user).order_by('-upvotes')
    if not posts:
        messages.error(request, 'You don\'t have any posts yet. Create your post')
        return redirect('bulletin:create-bulletin')
    else:
        context = {
            'posts': posts
        }
        
        return render(
            request, 
            'views/bulletin/manage_posts.html',
            context
        )

@login_required
def delete_post(request, bulletin_id):
    try:
        bulletin = Bulletin.objects.get(object_id=bulletin_id)
    except:
        raise Http404
    
    if not bulletin.user == request.user:
        raise Http404

    else:
        bulletin.delete()
        messages.success(request, 'Your post has been deleted')
        return redirect('bulletin:manage-posts')