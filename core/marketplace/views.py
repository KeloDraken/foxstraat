from django.contrib import messages
from utils.helpers import object_id_generator
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render

from core.marketplace.forms import AddTemplateListingForm
from core.marketplace.models import Template

@login_required
def storefront(request):
    listings = Template.objects.all()
    context = {
        'listings': listings
    }
    return render(request, 'views/marketplace/storefront.html', context)

@login_required
def add_listing(request):
    if request.method == 'POST':
        try:
            name = request.POST.get('name')
        except:
            messages.error(
                request, 'Couldn\'t add listing because of a name error')
            return redirect('marketplace:add-listing')
        try:
            description = request.POST.get('description')
        except:
            messages.error(request, 
                'Couldn\'t add listing because of a description error')
            return redirect('marketplace:add-listing')
        try:
            price = request.POST.get('price')
        except:
            messages.error(request, 
                'Couldn\'t add listing because of a price error')
            return redirect('marketplace:add-listing')
        try:
            template = request.POST.get('template')
        except:
            messages.error(request,    
                'Couldn\'t add listing because of a CSS error')
            return redirect('marketplace:add-listing')

        if request.FILES.get('screenshot'):
            screenshot = request.FILES.get('screenshot')
        else:
            messages.error(request, 
                'Couldn\'t add listing because of a screeshot error')
            return redirect('marketplace:add-listing')

        user = request.user
        object_id = object_id_generator(size=11, model=Template)

        Template.objects.create(
            object_id=object_id,
            user=user,
            name=name,
            description=description,
            price=price,
            template=template,
            screenshot_1=screenshot
        )

        messages.success(request, 'Successfully added listing')
        return redirect('/')
        
    return render(
        request,
        'views/marketplace/add_listing.html', 
    )