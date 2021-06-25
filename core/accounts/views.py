from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.views import LoginView
from django.contrib.auth.decorators import login_required
from django.http.response import Http404

from django.shortcuts import redirect, render

from core.accounts.forms import (
    UserLoginForm,
    UserRegistrationForm
)
from core.accounts.models import User


def user_registration(request):
    if request.user.is_authenticated:
        return redirect('accounts:user-dashboard')
    else:
        if request.method =='POST':
            registration_form = UserRegistrationForm(request.POST)
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
            registration_form = UserRegistrationForm()

        return render(
            request, 
            'views/auth/registration_form.html', 
            {'registration_form': registration_form}
        )


class UserLoginView(LoginView):
    template_name = 'views/auth/login_form.html'
    authentication_form = UserLoginForm
    redirect_authenticated_user = True

user_login = UserLoginView.as_view()


def user_logout(request):
    logout(request)
    return redirect('/')


@login_required
def user_dashboard(request):
    user = request.user
    context = {
        'user': user
    }
    return render(request, 'views/accounts/dashboard.html', context)


def get_user_profile(request, username):
    try:
        user = User.objects.get(username=username)
        context = {
            'user': user
        }
        return render(request, 'views/accounts/user_profile.html', context)
    except:
        raise Http404()

@login_required
def edit_user_profile(request):
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
            bio = request.POST['about_me']

            user.bio = bio
            user.custom_styles = custom_styles
            user.save()

            messages.success(request, 'Profile successfully updated')
        
    context = {
        'user': request.user,
    }
    return render(request, 'views/accounts/edit_profile.html', context)