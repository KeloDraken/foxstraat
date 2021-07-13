from utils.helpers import ref_from_url
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.views import LoginView
from django.contrib.auth.decorators import login_required
from django.http.response import Http404

from django.shortcuts import redirect, render

from core.forms import FormWithCaptcha

from core.accounts.forms import (
    UserLoginForm,
    UserRegistrationForm
)
from core.accounts.models import User
from core.announcements.models import Announcement
from core.bulletin.models import Bulletin, BulletinImage


def user_registration(request):
    ref_from_url(request)
    if request.user.is_authenticated:
        return redirect('accounts:user-dashboard')
    else:
        captcha = FormWithCaptcha

        if request.method =='POST':
            registration_form = UserRegistrationForm(request.POST)

            # TODO: remove this try/catch in production
            try:
                captcha_data = request.POST['g-recaptcha-response']
            except:
                captcha_data = '...'
            
            if not captcha_data == '':
                if registration_form.is_valid():
                    registration_form.save()

                    username = request.POST['username']
                    password = request.POST['password2']

                    user = authenticate(username=username.lower(), password=password)

                    if user is not None:
                        login(request, user)
                        messages.success(
                            request, 
                            'Welcome to Foxstraat. Feel free to explore.')
                        return redirect('accounts:user-dashboard')
                    else:
                        pass
            else:
                messages.error(request, 'Please confirm that you\'re not a robot')
        else:
            registration_form = UserRegistrationForm()

        context = {
            'registration_form': registration_form,
            'captcha': captcha,
        }
        return render(
            request, 
            'views/auth/registration_form.html', 
            context
        )


class UserLoginView(LoginView):
    template_name = 'views/auth/login_form.html'
    authentication_form = UserLoginForm
    redirect_authenticated_user = True

user_login = UserLoginView.as_view()

@login_required
def user_logout(request):
    logout(request)
    return redirect('accounts:user-login')


@login_required
def user_dashboard(request):
    ref_from_url(request)
    announcements = Announcement.objects.all().order_by('-datetime_created')
    posts = Bulletin.objects.all().exclude(user=request.user).order_by('?')[:3]
    context = {
        'posts': posts,
        'announcements': announcements,
    }
    return render(request, 'views/dashboard/dashboard.html', context)


def get_user_profile(request, username):
    ref_from_url(request)
    user = User.objects.get(username=username)
    if user.is_active:
        posts = Bulletin.objects.filter(user=user).order_by('-datetime_created')

        context = {
            'posts': posts,
            'user': user
        }
        return render(request, 'views/accounts/user_profile.html', context)
    else:
        raise Http404

@login_required
def edit_user_profile(request):
    ref_from_url(request)
    if request.method == 'POST':
        custom_styles = request.POST['custom_styles']
        
        if '<script>' in custom_styles \
        or '</script>' in custom_styles \
        or '<SCRIPT>' in custom_styles \
        or '</SCRIPT>' in custom_styles :
            context = {
                'user': request.user,
            }
            messages.error(
                request, 
                '''
                Only css is allowed.
                Your account has been placed on a watchlist. 
                Continued use of non-css code will result in a 
                permanent ban from Foxstraat.
                '''
            )
            return render(request, 'views/accounts/edit_profile.html', context)
        else:
            user = request.user

            if request.FILES.get('profile_pic'):
                user.profile_pic = request.FILES.get('profile_pic')
            
            bio = request.POST['about_me']

            if len(bio) > 220:
                messages.error(
                    request, 
                    'Your bio is too long. Please keep it at 220 characters of less'
                )
            else:
                user.bio = bio
            
            instagram = request.POST['instagram']
            if not len(instagram) <= 0 and not instagram == None:
                user.instagram = instagram
            else:
                user.instagram = None

            twitter = request.POST['twitter']
            if not len(twitter) <= 0 and not twitter == None:
                user.twitter = twitter
            else:
                user.twitter = None

            website = request.POST['website']
            if not len(website) <= 0 and not website == None:
                user.website = website
            else:
                user.website = None

            if not len(custom_styles) <= 0 and not custom_styles == None:
                user.custom_styles = custom_styles
                user.save()
            else:
                pass

            messages.success(request, 'Profile successfully updated')
        
    context = {
        'user': request.user,
    }
    return render(request, 'views/accounts/edit_profile.html', context)

@login_required
def delete_account(request):
    ref_from_url(request)
    if request.user.is_superuser:
        messages.error(request, 'Admins need to use the admin site to delete their accounts')
        return redirect('accounts:user-dashboard')
    else:
        messages.success(request, 'You account has been deleted')
        request.user.is_active = False
        request.user.save()
        return user_logout(request)