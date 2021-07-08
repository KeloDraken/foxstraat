from django.contrib.auth.decorators import login_required
from django.shortcuts import render


@login_required
def storefront(request):
    return render(request, 'views/marketplace/storefront.html')