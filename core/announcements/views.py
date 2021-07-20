from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http.response import Http404 
from django.shortcuts import redirect, render

from utils.helpers import object_id_generator

from core.announcements.forms import AnnouncementCreationForm, ProductAnnouncementCreationForm
from core.announcements.models import Announcement, ProductAnnouncement

@login_required
def create_announcement(request):
    if not request.user.is_superuser:
        raise Http404()
    else:
        if request.method == 'POST':
            form = AnnouncementCreationForm(request.POST)
            if form.is_valid():
                form.save(commit=False)
                object_id = object_id_generator(size=11, model=Announcement)
                form.object_id = object_id
                form.save()

                messages.success(request, 'New announcement added')
                return redirect('accounts:user-dashboard')
            else:
                messages.error(request, 'Announcement creation failed')
        
        else:
            form = AnnouncementCreationForm()

        context = {
            'form': form,
        }
        return render(
            request, 
            'views/announcements/create_announcement.html', 
            context
        )


@login_required
def create_product_announcement(request):
    if not request.user.is_superuser:
        raise Http404()
    else:
        if request.method == 'POST':
            form = ProductAnnouncementCreationForm(request.POST)
            if form.is_valid():
                form.save(commit=False)
                object_id = object_id_generator(size=11, model=ProductAnnouncement)
                form.object_id = object_id
                form.save()

                messages.success(request, 'New announcement added')
                return redirect('accounts:user-dashboard')
            else:
                messages.error(request, 'Announcement creation failed')
        
        else:
            form = ProductAnnouncementCreationForm()

        context = {
            'page': 'product',
            'form': form,
        }
        return render(
            request, 
            'views/announcements/create_announcement.html', 
            context
        )

