from django.contrib.auth.decorators import login_required
from django.shortcuts import render


@login_required
def search(request):
    query = request.GET.get('q')
    if query:
        context = {
            'query': query
        }
        return render(request, 'views/search/results.html', context)
    else:
        return render(request, 'views/search/search.html')