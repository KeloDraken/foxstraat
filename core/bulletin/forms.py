from django import forms

from core.bulletin.models import (
    Bulletin,
    BulletinImage,
)

class CreateBulletinForm(forms.ModelForm):
    title = forms.CharField(
        max_length=20, 
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
    yt_embed = forms.CharField(
        max_length=11, 
        label='', 
        widget=forms.TextInput(
            attrs={
                'class': 'form-input',
                'placeholder': 'You can embed a YouTube video by submitting the video id',
                'autocomplete': 'off',
                'autofocus': 'true',
                'autocapitalize': 'off'
            }
        )
    ) 
    caption = forms.CharField(widget=forms.Textarea(
        attrs={
            'cols': 100,
            'class': 'form-input',
            'placeholder': 'Write your caption/bulletin',
            'required': 'false',
            'rows': 100,
        }
    ))
    class Meta:
        model = Bulletin
        fields = ('title','yt_embed','caption',)
 
 
class BulletinImageForm(forms.ModelForm):
    image = forms.ImageField(widget=forms.FileInput(
        attrs={
            'onchange': 'processImage()',
            'id': 'selected-image',
            'required': 'false'
        }
    ))
    class Meta:
        model = BulletinImage
        fields = ('image',)