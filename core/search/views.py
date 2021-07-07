from django.contrib.auth.decorators import login_required
from django.shortcuts import render


@login_required
def search(request):
    try:
        query = request.GET['query']
        context = {
            'query': query
        }
        return render(request, 'views/search/results.html', context)
    except:
        return render(request, 'views/search/search.html')