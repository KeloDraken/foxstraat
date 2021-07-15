from django import forms

from core.bulletin.models import (
    Bulletin
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
 
