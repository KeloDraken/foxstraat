from django import forms

from core.bulletin.models import (
    Bulletin,
    Song,
)

class CreateBulletinForm(forms.ModelForm):
    title = forms.CharField(
        max_length=140, 
        label='', 
        widget=forms.TextInput(
            attrs={
                'class': 'form-input',
                'placeholder': 'Give your post a short title',
                'autocomplete': 'off',
                'autofocus': 'true',
                'autocapitalize': 'off'
            }
        )
    ) 
    caption = forms.CharField(required=False, widget=forms.Textarea(
        attrs={
            'cols': 100,
            'class': 'form-input',
            'placeholder': 'Write your caption...',
            'rows': 100,
        }
    ))
    image = forms.ImageField(
        required=False, 
        widget=forms.FileInput(
            attrs={
                'required': 'false',
                'onchange': 'processImage()',
                'id': 'selected-image',
                'required': 'false'
            }
        )
    )
    class Meta:
        model = Bulletin
        fields = (
            'title',
            'caption',
            'image',
        )
 
 
class AddSongForm(forms.ModelForm):
    title = forms.CharField(
        max_length=140, 
        label='', 
        widget=forms.TextInput(
            attrs={
                'class': 'form-input',
                'placeholder': 'Give your post a short title',
                'autocomplete': 'off',
                'autofocus': 'true',
                'autocapitalize': 'off'
            }
        )
    ) 
    spotify = forms.URLField(
        required=False,
        max_length=140, 
        label='', 
        widget=forms.TextInput(
            attrs={
                'class': 'form-input',
                'placeholder': 'Give your post a short title',
                'autocomplete': 'off',
                'autofocus': 'true',
                'autocapitalize': 'off'
            }
        )
    ) 
    soundcloud = forms.URLField(
        required=False,
        max_length=140, 
        label='', 
        widget=forms.TextInput(
            attrs={
                'class': 'form-input',
                'placeholder': 'Give your post a short title',
                'autocomplete': 'off',
                'autofocus': 'true',
                'autocapitalize': 'off'
            }
        )
    ) 
    youtube = forms.URLField(
        required=False,
        max_length=140, 
        label='', 
        widget=forms.TextInput(
            attrs={
                'class': 'form-input',
                'placeholder': 'Give your post a short title',
                'autocomplete': 'off',
                'autofocus': 'true',
                'autocapitalize': 'off'
            }
        )
    ) 
    cover_art = forms.ImageField(
        required=False, 
        widget=forms.FileInput(
            attrs={
                'required': 'false',
                'onchange': 'processImage()',
                'id': 'selected-image',
                'required': 'false'
            }
        )
    )
    class Meta:
        model = Song
        fields = (
            'title',
            'spotify',
            'soundcloud',
            'youtube',
            'cover_art',
        )
 
 