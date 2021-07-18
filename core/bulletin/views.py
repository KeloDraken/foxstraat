import calendar
import random
from datetime import date

from django.contrib import messages
from django.contrib.auth.decorators import login_required

from django.core.paginator import Paginator

from django.http.response import (
    Http404,
    HttpResponseBadRequest, 
    HttpResponseForbidden, 
    JsonResponse
)
from django.shortcuts import get_object_or_404, redirect, render

from utils.helpers import (
    extract_hashtags,
    link_tags_to_post, 
    object_id_generator
)

from core.forms import FormWithCaptcha

from core.bulletin.forms import CreateBulletinForm
from core.bulletin.models import Bulletin, Vote


def check_has_user_voted(user, bulletin):
    try:
        Vote.objects.get(user=user, bulletin=bulletin)
        return True

    except Vote.DoesNotExist:
        return False

def _cast_vote(bulletin, vote_value, vote):
    vote.has_voted = True
    # Upvote
    if vote_value == 1:
        vote.value = vote_value
        bulletin.upvotes = bulletin.upvotes + 1
        bulletin.score = bulletin.score + 1
        bulletin.save()
        vote.save()
    # Downvote
    elif vote_value == -1:
        vote.value = vote_value
        bulletin.downvotes = bulletin.downvotes + 1
        bulletin.score = bulletin.score - 1
        bulletin.save()
        vote.save()
    # Cancel vote
    elif vote_value == 0:
        # If user previously downvoted the post
        if vote.value == -1:
            vote.value = 0
            bulletin.downvotes = bulletin.downvotes - 1
            bulletin.score = bulletin.score + 1
            bulletin.save()
            vote.save()  

        # If user previously upvoted the post
        elif vote.value == 1:
            vote.value = 0
            bulletin.upvotes = bulletin.upvotes - 1
            bulletin.score = bulletin.score - 1
            bulletin.save()
            vote.save()  
        elif vote.value == 0:
            pass

    else:
        return HttpResponseBadRequest()


def cast_vote(request, bulletin_id):
    if not request.user.is_authenticated:
        return HttpResponseForbidden()
    else:
        bulletin = get_object_or_404(Bulletin, object_id=bulletin_id)
        
        try:
            vote_value = int(request.GET.get('vote_value'))
        except:
            vote_value = 0

        has_user_voted = check_has_user_voted(request.user, bulletin)

        if has_user_voted == True:
            vote = Vote.objects.get(
                user=request.user,
                bulletin=bulletin
            )
            if vote.value == -1 or vote.value == 1:
                _cast_vote(bulletin=bulletin, vote_value=0, vote=vote)
            elif vote.value == 0:
                _cast_vote(bulletin=bulletin, vote_value=vote_value, vote=vote)  

            return JsonResponse({
                'score': bulletin.score,
                'has_voted': True
            })
        elif has_user_voted == False:
            vote = Vote.objects.create(
                    user=request.user,
                    bulletin=bulletin
            )
            _cast_vote(bulletin, vote_value, vote)
            return JsonResponse({
                    'score': bulletin.score,
                    'has_voted': True
                })

@login_required
def create_bulletin(request):
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
                
                request.user.num_posts = request.user.num_posts + 1
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
    post = get_object_or_404(Bulletin, object_id=bulletin_id)

    more_from_user = Bulletin.objects.filter(
        user=post.user
    ).order_by('?')[:4]

    # upvotes = post.upvotes / random.randint(1,20)
    context = {
        'has_voted': check_has_user_voted(request.user, post),
        'post': post,
        'upvotes': post.score,
        'more_from_user': more_from_user
    }
    return render(
        request, 
        'views/bulletin/view_bulletin.html', 
        context
    )

def frontpage(request):
    post_objects = Bulletin.objects.all().order_by('-upvotes')

    paginator = Paginator(post_objects, 20)
    
    try:
        page_number = int(request.GET.get('sida'))
    except:
        page_number = 1
    
    page_obj = paginator.get_page(page_number)

    current_date = date.today()
    weekday = calendar.day_name[current_date.weekday()]

    context = {
        'heading': f'Explore {weekday}\'s photos',
        'page_obj': page_obj
    }
    
    return render(
        request, 
        'views/frontpage/frontpage.html',
        context
    )

@login_required
def manage_posts(request):
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