from django.contrib.auth import logout
from django.contrib.auth.views import LoginView
from django.contrib.auth.decorators import login_required

from django.shortcuts import redirect, render

from core.accounts.forms import (
    UserLoginForm,
    UserRegistrationForm
)


def user_registration(request):
    if request.user.is_authenticated:
        return redirect('accounts:user-dashboard')
    else:
        if request.method =='POST':
            registration_form = UserRegistrationForm(request.POST)
            if registration_form.is_valid():
                registration_form.save()
                return redirect('accounts:user-dashboard')
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