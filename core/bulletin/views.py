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

from core.bulletin.forms import CreateBulletinForm
from core.bulletin.models import (
    Bulletin,
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
                
                return redirect('bulletin:get-bulletin', bulletin_id=object_id)

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

def get_bulletin(request, bulletin_id):
    ref_from_url(request)
    post = get_object_or_404(Bulletin, object_id=bulletin_id)

    if request.user.is_authenticated:
        post.upvotes += 1
        post.save()

    more_from_user = Bulletin.objects.filter(
        user=post.user
    ).order_by('?')[:4]

    context = {
        'post': post,
        'more_from_user': more_from_user
    }
    return render(
        request, 
        'views/bulletin/view_bulletin.html', 
        context
    )

def frontpage(request):
    ref_from_url(request)
    posts = Bulletin.objects.all().order_by('-upvotes')

    topics = Tag.objects.all().order_by('?')[:30]
    context = {
        'topics': topics,
        'posts': posts
    }
    
    return render(
        request, 
        'views/frontpage/frontpage.html',
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