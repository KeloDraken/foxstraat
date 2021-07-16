from django import forms 

from core.blog.models import Blog


class CreateBlogPostForm(forms.ModelForm):
    title = forms.CharField(
        max_length=1000, 
        required=True, 
        widget=forms.TextInput(
            attrs={
                'class': 'form-input',
                'placeholder': 'Your post\'s title',
                'autocomplete': 'off',
                'autofocus': 'true',
                'autocapitalize': 'off'
            }
        )
    ) 
    body = forms.CharField(required=True, widget=forms.Textarea(
        attrs={
            'cols': 100,
            'class': 'form-input',
            'placeholder': 'Write your blog\'s content here...',
            'rows': 100,
        }
    ))

    class Meta:
        model = Blog
        fields = (
            'title',
            'body',
        )