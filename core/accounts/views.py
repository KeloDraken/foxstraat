from django.shortcuts import redirect, render
from core.accounts.forms import UserRegistrationForm


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