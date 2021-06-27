from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.forms import modelformset_factory
from django.shortcuts import redirect, render

from utils.helpers import object_id_generator

from core.forms import FormWithCaptcha

from core.bulletin.forms import (
    CreateBulletinForm,
    BulletinImageForm,
)
from core.bulletin.models import Bulletin, BulletinImage


@login_required
def create_bulletin(request):
    if not request.user.is_authenticated:
        return redirect('accounts:user-login')
    else:
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
            
            captcha_data = request.POST['g-recaptcha-response']
            if not captcha_data == '':
                if post_form.is_valid() and formset.is_valid():
                    post_form = post_form.save(commit=False)
                    post_form.user = request.user

                    object_id = object_id_generator(11, Bulletin)
                    post_form.object_id = object_id
                    post_form.save()

                    for form in formset.cleaned_data:
                        if form:
                            image = form['image']
                            photo = BulletinImage(bulletin=post_form, image=image)
                            photo.save()

                    return redirect(f'/b/{object_id}')

                else:
                    print(post_form.errors, formset.errors)
            else:
                messages.error(request, 'Please confirm that you\'re not a robot')
        else:
            post_form = CreateBulletinForm()
            formset = ImageFormSet(queryset=BulletinImage.objects.none())

        context = {
            'post_form': post_form, 
            'formset': formset,
            'captcha': captcha,
        }
        return render(request, 'views/bulletin/create_bulletin.html', context)


def explore_bulletins(request):
    return render(
        request, 
        'views/bulletin/explore_bulletins.html',
    )