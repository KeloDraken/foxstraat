from django import forms

from core.bulletin.models import (
    Bulletin,
    BulletinImage,
)

class CreateBulletinForm(forms.ModelForm): 
    class Meta:
        model = Bulletin
        fields = ('caption',)
 
 
class BulletinImageForm(forms.ModelForm):
    class Meta:
        model = BulletinImage
        fields = ('image',)