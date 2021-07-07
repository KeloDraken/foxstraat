from django import forms 
from core.announcements.models import Announcement


class AnnouncementCreationForm(forms.ModelForm):
    class Meta:
        model = Announcement
        fields = (
            'title',
            'body',
        )

        