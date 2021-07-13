from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render

from utils.helpers import object_id_generator, ref_from_url

from core.marketplace.models import Template

@login_required
def storefront(request):
    ref_from_url(request)
    listings = Template.objects.all()
    context = {
        'listings': listings
    }
    return render(request, 'views/marketplace/storefront.html', context)

@login_required
def add_listing(request):
    ref_from_url(request)
    if request.method == 'POST':
        try:
            name = request.POST.get('name')
            if not len(name) <= 0 and not name == None:
                pass
            else:
                messages.error(
                request, 'Couldn\'t add listing because of a name error')
                return redirect('marketplace:add-listing')
        except:
            messages.error(
                request, 'Couldn\'t add listing because of a name error')
            return redirect('marketplace:add-listing')
          
        try:
            description = request.POST.get('description')
            if not len(description) <= 0 and not description == None:
                pass
            else:
                messages.error(request, 
                'Couldn\'t add listing because of a description error')
                return redirect('marketplace:add-listing')
        except:
            messages.error(request, 
                'Couldn\'t add listing because of a description error')
            return redirect('marketplace:add-listing')
            
        try:
            price = request.POST.get('price')
            if not len(price) <= 0 and not price == None:
                try:
                    price = int(price)
                except:
                    messages.error(request, 
                    'Couldn\'t add listing because of a price error')
                    return redirect('marketplace:add-listing')
            else:
                messages.error(request, 
                'Couldn\'t add listing because of a price error')
                return redirect('marketplace:add-listing')
        except:
            messages.error(request, 
                'Couldn\'t add listing because of a price error')
            return redirect('marketplace:add-listing')
        
        try:
            template = request.POST.get('template')            
            if not len(price) <= 0 and not price == None:
                if '<script>' in template \
                or '</script>' in template \
                or '<SCRIPT>' in template \
                or '</SCRIPT>' in template :
                    messages.error(
                        request, 
                        '''
                        Only css is allowed.
                        Your account has been placed on a watchlist. 
                        Continued use of non-css code will result in a 
                        permanent ban from Foxstraat.
                        '''
                    )
                    return redirect('marketplace:add-listing')
            else:
                messages.error(request,    
                'Couldn\'t add listing because of a CSS error')
                return redirect('marketplace:add-listing')
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

@login_required
def view_listing(request, listing_id):
    ref_from_url(request)
    post = Template.objects.get(object_id=listing_id)

    context = {
        'post': post
    }
    return render(
        request, 
        'views/marketplace/view_listing.html', 
        context
    )
