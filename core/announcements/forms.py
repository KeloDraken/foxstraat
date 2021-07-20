from django import forms 
from core.announcements.models import Announcement, ProductAnnouncement


class AnnouncementCreationForm(forms.ModelForm):
    title = forms.CharField(
        max_length=140, 
        label='', 
        widget=forms.TextInput(
            attrs={
                'class': 'form-input',
                'placeholder': 'Give the announcement a short title',
                'autocomplete': 'off',
                'autofocus': 'true',
                'autocapitalize': 'off'
            }
        )
    ) 
    body = forms.CharField(required=False, widget=forms.Textarea(
        attrs={
            'cols': 100,
            'class': 'form-input',
            'placeholder': 'Write the announcement body...',
            'rows': 100,
        }
    ))
    class Meta:
        model = Announcement
        fields = (
            'title',
            'body',
        )

class ProductAnnouncementCreationForm(forms.ModelForm):
    title = forms.CharField(
        max_length=140, 
        label='', 
        widget=forms.TextInput(
            attrs={
                'class': 'form-input',
                'placeholder': 'Give the announcement a short title',
                'autocomplete': 'off',
                'autofocus': 'true',
                'autocapitalize': 'off'
            }
        )
    ) 
    body = forms.CharField(required=False, widget=forms.Textarea(
        attrs={
            'cols': 100,
            'class': 'form-input',
            'placeholder': 'Write the announcement body...',
            'rows': 100,
        }
    ))
    class Meta:
        model = ProductAnnouncement
        fields = (
            'title',
            'body',
        )

        