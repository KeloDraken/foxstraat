from django.shortcuts import render


def index(request):
    if not request.user.is_authenticated:
        return render(request, 'index.html')
    else:
        context = {
            'user': request.user,
        }
        return render(request, 'index.html', context)