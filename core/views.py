from django.shortcuts import redirect, render

from utils.helpers import ref_from_url

def index(request):
    ref_from_url(request)
    if request.user.is_authenticated:
        return redirect('accounts:user-dashboard')
    else:
        return render(request, 'views/index.html')


def about(request):
    ref_from_url(request)
    return render(request, 'views/index.html')
