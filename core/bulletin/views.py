from django.contrib import messages
from django.contrib.auth.decorators import login_required

from django.forms import modelformset_factory
from django.shortcuts import redirect, render

from utils.helpers import (
    extract_hashtags,
    link_tags_to_post, 
    object_id_generator
)

from core.forms import FormWithCaptcha

from core.bulletin.forms import (
    CreateBulletinForm,
    BulletinImageForm,
)
from core.bulletin.models import (
    Bulletin, 
    BulletinImage,
    Tag
)


@login_required
def create_bulletin(request):
    captcha = FormWithCaptcha

    ImageFormSet = modelformset_factory(
        BulletinImage, 
        form=BulletinImageForm, 
        extra=1
    )    
    
    if request.method == 'POST':
        post_form = CreateBulletinForm(request.POST)
        formset = ImageFormSet(
            request.POST, 
            request.FILES,
            queryset=BulletinImage.objects.none()
        )
        
        # TODO: remove this try/catch in production
        try:
            captcha_data = request.POST['g-recaptcha-response']
        except:
            captcha_data = '...'
            
        if not captcha_data == '':
            if post_form.is_valid() and formset.is_valid():
                post_form = post_form.save(commit=False)
                post_form.user = request.user

                object_id = object_id_generator(11, Bulletin)
                post_form.object_id = object_id
                
                caption = request.POST['caption']
                
                hashtags = extract_hashtags(text=caption)

                request.user.num_posts =+ 1
                request.user.save()
                post_form.save()

                for form in formset.cleaned_data:
                    if form:
                        image = form['image']
                        photo = BulletinImage(bulletin=post_form, image=image)
                        photo.save()

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
        formset = ImageFormSet(queryset=BulletinImage.objects.none())

    context = {
        'post_form': post_form, 
        'formset': formset,
        'captcha': captcha,
    }
    return render(
        request, 
        'views/bulletin/create_bulletin.html', 
        context
    )


def get_bulletin(request, bulletin_id):
    bulletin = Bulletin.objects.get(object_id=bulletin_id)
    post = BulletinImage.objects.get(bulletin=bulletin)

    if request.user.is_authenticated:
        post.upvotes += 1
        post.save()

    user_bulletins = Bulletin.objects.filter(
        user=bulletin.user
    ).order_by('?')[:2]
    
    more_from_user = []
    for i in user_bulletins:
        obj =  BulletinImage.objects.filter(bulletin=i)
        more_from_user.append(obj)
        
    context = {
        'post': post,
        'more_from_user': more_from_user,
    }
    return render(
        request, 
        'views/bulletin/view_bulletin.html', 
        context
    )

def explore_bulletins(request):
    posts = BulletinImage.objects.all().order_by('-upvotes')

    topics = Tag.objects.all()
    context = {
        'topics': topics,
        'posts': posts
    }
    
    return render(
        request, 
        'views/bulletin/explore_bulletins.html',
        context
    )