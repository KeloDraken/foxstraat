from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render

from core.forms import FormWithCaptcha

from core.blog.forms import CreateBlogPostForm
from core.blog.models import Blog

from utils.helpers import ref_from_url


@login_required
def add_blog_post(request):
    ref_from_url(request)
    if not request.user.is_artist:
        messages.error(request, 'You\'re not an artist yet. Go to Edit profile to convert your account')
        return redirect('index')
    else:
        captcha = FormWithCaptcha()

        if request.method == 'POST':
            post_form = CreateBlogPostForm(request.POST)
            # TODO: remove this try/catch in production
            try:
                captcha_data = request.POST['g-recaptcha-response']
            except:
                captcha_data = '...'
                
            if not captcha_data == '':
                
                pass
            else:
                messages.error(
                    request, 
                    'Please confirm that you\'re not a robot'
                )
        else:
            post_form = CreateBlogPostForm()

        context = {
            'post_form': post_form,
            'captcha': captcha,
        }
        return render(
            request, 
            'views/blog/add_blog_post.html', 
            context
        )


def get_blog(request):
    pass
