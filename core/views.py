from django.shortcuts import redirect, render


def index(request):
    if request.user.is_authenticated:
        return redirect('accounts:user-dashboard')
    else:
        return render(request, 'views/index.html')


def about(request):
    return render(request, 'views/index.html')
