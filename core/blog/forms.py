from django import forms 

from core.blog.models import Blog


class CreateBlogPostForm(forms.ModelForm):
    class Meta:
        model = Blog
        fields = (
            'title',
            'body',
        )