from django import forms
from django.contrib.auth.forms import UserCreationForm

from core.accounts.models import User


class UserRegistrationForm(UserCreationForm):

    class Meta:
        model = User
        fields = (
            'username',
            'password1',
            'password2'
        )

    def save(self, commit=True):
        user = super(UserRegistrationForm, self).save(commit=False)
        if commit:
            user.save()
        return user