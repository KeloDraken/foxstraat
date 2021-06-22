from django.contrib.auth.views import LoginView
from django.shortcuts import redirect, render

from core.accounts.forms import (
    UserLoginForm,
    UserRegistrationForm
)


def user_registration(request):
    if request.method =='POST':        
        registration_form = UserRegistrationForm(request.POST)
        if registration_form.is_valid():
            registration_form.save()
            return redirect('/')
    else:
        registration_form = UserRegistrationForm()

    return render(
        request, 
        'auth/registration_form.html', 
        {'registration_form': registration_form}
    )


class UserLoginView(LoginView):
    template_name = 'auth/login_form.html'
    authentication_form = UserLoginForm

user_login = UserLoginView.as_view()