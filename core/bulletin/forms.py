from django import forms

from core.bulletin.models import (
    Bulletin,
    BulletinImage,
)

class CreateBulletinForm(forms.ModelForm): 
    caption = forms.CharField(widget=forms.Textarea(
        attrs={
            'cols': 100,
            'rows': 100,
        }
    ))
    class Meta:
        model = Bulletin
        fields = ('caption',)
 
 
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