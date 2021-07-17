import django
from django.db.models import Q 
from django.contrib.auth.decorators import login_required
from django.shortcuts import render

from core.accounts.models import User
from core.bulletin.models import Bulletin

@login_required
def advanced_search(request):
    search_query = request.GET.get('q')
    if search_query:
        search_models = [User, Bulletin]
        search_results = []
        final_results = []

        for model in search_models:
            fields = [x for x in model._meta.fields if isinstance(x , django.db.models.CharField)]
            search_queries = [Q(**{x.name+'__contains': search_query}) for x in fields]
            q_object = Q()

            for query in search_queries:
                q_object = q_object | query
            
            results = model.objects.filter(q_object)
            search_results.append(results)

            for i in search_results:
                final_results.append(i)

        context = {
            'query': search_query,
            'results': final_results
        }
        return render(request, 'views/search/results.html', context)
    else:
        return render(request, 'views/search/search.html')

def search(request):
    search_query = request.GET.get('q')
    if search_query:
        results = User.objects.filter(
            Q(username__icontains=search_query)|
            Q(display_name__icontains=search_query)|
            Q(bio__icontains=search_query)
        ).order_by('-last_login').exclude(is_active=False)[:20]
        context = {
            'query': search_query,
            'results': results
        }
        return render(request, 'views/search/results.html', context)
    else:
        return render(request, 'views/search/search.html')

