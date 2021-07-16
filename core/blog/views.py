from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render

from core.forms import FormWithCaptcha

from core.blog.forms import CreateBlogPostForm
from core.blog.models import Blog

from utils.helpers import object_id_generator, ref_from_url


@login_required
def add_blog_post(request):
    ref_from_url(request)
    if not request.user.is_blogger:
        messages.error(request, 'You\'re not a blogger yet. Go to Edit profile to add feature to your account')
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
                if post_form.is_valid():
                    post_form = post_form.save(commit=False)
                    post_form.user = request.user

                    object_id = object_id_generator(11, Blog)
                    post_form.object_id = object_id
                    post_form.save()

                    return redirect('blog:get-blog', blog_id=object_id)

                else:
                    messages.error(
                        request, 
                        'An error occured. Couldn\'t save your post'
                    )
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


def get_blog(request, blog_id):
    blog = get_object_or_404(Blog, object_id=blog_id)
    context = {
        'blog': blog,
    }
    return render(request, 'views/blog/view_blog.html', context)