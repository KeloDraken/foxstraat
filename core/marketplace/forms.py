from django import forms

from core.marketplace.models import Template


class AddTemplateListingForm(forms.ModelForm):
    class Meta:
        model = Template
        fields = (
            'name',
            'description',
            'screenshot_1',
            'screenshot_2',
            'price',
            'template'
        )