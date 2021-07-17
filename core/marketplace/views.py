from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http.response import Http404
from django.shortcuts import redirect, render

from utils.helpers import object_id_generator

from core.accounts.models import User
from core.marketplace.models import Template

@login_required
def storefront(request):
    listings = Template.objects.all().order_by('?')
    context = {
        'listings': listings
    }
    return render(request, 'views/marketplace/storefront.html', context)

@login_required
def add_listing(request):
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
def manage_listings(request):
    posts = Template.objects.filter(user=request.user)
    if not posts:
        messages.error(
            request, 
            'You don\'t have any marketplace listings. Create your listing'
        )
        return redirect('marketplace:add-listing')
    else:
        context = {
            'posts': posts
        }
        
        return render(
            request, 
            'views/marketplace/manage_listings.html',
            context
        )

@login_required
def delete_listing(request, listing_id):
    try:
        bulletin = Template.objects.get(object_id=listing_id)
    except:
        raise Http404
    
    if not bulletin.user == request.user:
        raise Http404

    else:
        bulletin.delete()
        messages.success(request, 'Your post has been deleted')
        return redirect('marketplace:manage-listing')

@login_required
def view_listing(request, listing_id):
    post = Template.objects.get(object_id=listing_id)

    context = {
        'post': post
    }
    return render(
        request, 
        'views/marketplace/view_listing.html', 
        context
    )

@login_required
def buy_template(request, listing_id):
    if request.method == 'POST':
        try:
            styles = request.POST.get('template')
        except:
            messages.error(request, 'Couldn\'t apply styles')

        request.user.custom_styles = styles
        request.user.save()
        messages.success(request, 'Template has been applied to your profile')
        return redirect('get-user-profile', username=request.user.username)
    
    else:
        try:
            template = Template.objects.get(object_id=listing_id)
        except:
            raise Http404

        if request.user.gelt < template.price:
            messages.error(
                request, 
                'You don\'t have enough gelt to buy this template.\
                    You can earn gelt by posting and browsing Foxstraat \
                or by selling your own templates'
            )
            return redirect('marketplace:view-listing', listing_id=listing_id)
        else:
            creator = User.objects.get(username=template.user.username)
            creator.gelt += template.price
            creator.save()

            request.user.gelt-= template.price
            request.user.save()

        messages.success(
            request, 
            'You\'ve successfully bought access to this template. \
            Copy the CSS into the Customise Profile section of \
            the edit profile page or click Apply Styles')
        context = {
            'template': template
        }
        return render(
            request, 
            'views/marketplace/buy_template.html', 
            context
        )