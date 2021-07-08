from django.contrib import messages
from utils.helpers import object_id_generator
from django.contrib.auth.decorators import login_required
from django.shortcuts import render

from core.marketplace.forms import AddTemplateListingForm
from core.marketplace.models import Template

@login_required
def storefront(request):
    return render(request, 'views/marketplace/storefront.html')

@login_required
def add_listing(request):
    if request.method == 'POST':
        form = AddTemplateListingForm(request.POST)

        if form.is_valid():
            form = form.save(commit=False)
            form.user = request.user
            object_id = object_id_generator(11, Template)
            form.object_id = object_id
            form.save()

        else:    
            messages.error(request, 'Post creation failed')

    else:
        form = AddTemplateListingForm()

    context = {
        'form': form, 
    }
    return render(
        request, 
        'views/marketplace/add_listing.html', 
        context
    )