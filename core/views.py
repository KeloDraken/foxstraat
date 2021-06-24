from django.shortcuts import redirect, render


def index(request):
    if not request.user.is_authenticated:
        return render(request, 'index.html')
    else:
        return redirect('accounts:user-dashboard')