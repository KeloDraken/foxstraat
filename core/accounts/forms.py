from django import forms
from django.contrib.auth.forms import (
    AuthenticationForm, 
    UserCreationForm,
)
from django.core.exceptions import ValidationError

from core.accounts.models import User


class UserRegistrationForm(UserCreationForm):
    username = forms.CharField(max_length=20, label=None)
    password1 = forms.CharField(
        max_length=60, 
        label=None, 
        widget=forms.PasswordInput
    )
    password2 = forms.CharField(
        max_length=60, 
        label=None, 
        widget=forms.PasswordInput
    )

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

class UserLoginForm(AuthenticationForm):
    def confirm_login_allowed(self, user):
        if not user.is_active:
            raise ValidationError(
                "This account is inactive.",
                code='inactive',
            )