from django import forms
from django.forms import inlineformset_factory

from utils.db import object_id_generator

from core.bulletin.models import (
    Bulletin,
    BulletinImage,
)

ChildItemInlineFormset = inlineformset_factory(
    Bulletin, 
    BulletinImage, 
    fields=('image',), 
    extra=0
)

class CreateBulletinForm(forms.ModelForm):
    class Meta:
        model = Bulletin
        fields = (
            'caption',
        )

    def save(self, commit=True):
        bulletin = super(CreateBulletinForm, self).save(commit=False)
        object_id = object_id_generator(size=11, model=Bulletin)
        bulletin.object_id = object_id
        if commit:
            bulletin.save()
        return bulletin