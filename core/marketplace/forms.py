from django import forms

from core.marketplace.models import Template


class AddTemplateListingForm(forms.ModelForm):
    name = forms.CharField(
        max_length=140, 
        label='', 
        widget=forms.TextInput(
            attrs={
                'class': 'form-input',
                'placeholder': 'Give your template a name',
                'autocomplete': 'off',
                'autofocus': 'true',
                'autocapitalize': 'off'
            }
        )
    ) 
    description = forms.CharField(
        max_length=280, 
        label='', 
        widget=forms.TextInput(
            attrs={
                'class': 'form-input',
                'placeholder': 'Write a short description of the template',
                'autocomplete': 'off',
                'autofocus': 'true',
                'autocapitalize': 'off'
            }
        )
    ) 
    price = forms.IntegerField(
        label='', 
        widget=forms.TextInput(
            attrs={
                'type': 'number',
                'class': 'form-input price',
                'placeholder': 'How much gelt do you want for it?',
                'autocomplete': 'off',
                'autofocus': 'true',
                'autocapitalize': 'off'
            }
        )
    ) 
    template = forms.CharField(required=True, widget=forms.Textarea(
        attrs={
            'cols': 100,
            'class': 'form-input css-editor',
            'id': 'custom_styles',
            'placeholder': 'Write your caption...',
            'rows': 100,
        }
    ))
    class Meta:
        model = Template
        fields = (
            'name',
            'description',
            'price',
            'template',
            'screenshot_1',
            'screenshot_2',
        )