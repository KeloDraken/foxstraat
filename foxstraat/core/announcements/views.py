from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http.response import Http404
from django.shortcuts import redirect, render

from foxstraat.utils.helpers import object_id_generator

from foxstraat.core.announcements.forms import AnnouncementCreationForm

from foxstraat.core.announcements.models import Announcement


def save_announcement(form):
    form.save(commit=False)
    object_id = object_id_generator(size=11, model=Announcement)
    form.object_id = object_id
    form.save()


@login_required
def create_announcement(request):
    if not request.user.is_superuser:
        raise Http404()
    else:
        if request.method == "POST":
            form = AnnouncementCreationForm(request.POST)
            if form.is_valid():
                save_announcement(form)

                messages.success(request, "New announcement added")
                return redirect("accounts:user-dashboard")
            else:
                messages.error(request, "Announcement creation failed")

        else:
            form = AnnouncementCreationForm()

        context = {
            "form": form,
        }
        return render(request, "views/announcements/create_announcement.html", context)
