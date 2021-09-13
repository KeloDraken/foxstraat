from django import forms
from django.contrib.auth.forms import (
    AuthenticationForm,
    UserCreationForm,
)
from django.core.exceptions import ValidationError
from django.utils.translation import gettext, gettext_lazy as _

from foxstraat.core.accounts.models import User


class UserRegistrationForm(UserCreationForm):
    username = forms.CharField(
        max_length=20,
        label="",
        widget=forms.TextInput(
            attrs={
                "class": "w-full text-black px-3 py-2 mb-3 border-2 border-gray-300 rounded bg-white",
                "placeholder": "Pick a unique username",
                "autocomplete": "off",
                "autocapitalize": "off",
            }
        ),
    )
    password1 = forms.CharField(
        max_length=60,
        label="",
        widget=forms.PasswordInput(
            attrs={
                "class": "w-full text-black px-3 py-2 mb-3 border-2 border-gray-300 rounded bg-white",
                "placeholder": "Required",
                "id": "password",
                "autocomplete": "false",
                "autocapitalize": "off",
            }
        ),
    )
    password2 = forms.CharField(
        max_length=60,
        label="",
        widget=forms.PasswordInput(
            attrs={
                "class": "w-full text-black px-3 py-2 mb-3 border-2 border-gray-300 rounded bg-white",
                "placeholder": "Required",
                "id": "password",
                "autocomplete": "none",
                "autocapitalize": "off",
            }
        ),
    )

    class Meta:
        model = User
        fields = ("username", "password1", "password2")

    def save(self, commit=True):
        user = super(UserRegistrationForm, self).save(commit=False)
        username = self.cleaned_data["username"]
        user.display_name = username
        if commit:
            user.save()
        return user


class UserLoginForm(AuthenticationForm):
    username = forms.CharField(
        max_length=20,
        label="",
        widget=forms.TextInput(
            attrs={
                "class": "w-full text-black px-3 py-2 mb-3 border-2 border-gray-300 rounded bg-white",
                "placeholder": "Required",
                "autocomplete": "off",
                "name": "Username",
                "autocapitalize": "off",
                "autofocus": "true",
            }
        ),
    )
    password = forms.CharField(
        max_length=60,
        label="",
        widget=forms.PasswordInput(
            attrs={
                "class": "w-full text-black px-3 py-2 mb-3 border-2 border-gray-300 rounded bg-white",
                "placeholder": "Required",
                "id": "password",
                "name": "Password",
                "autocomplete": "false",
                "autocapitalize": "off",
            }
        ),
    )
    error_messages = {
        "invalid_login": _("Incorrect log in credentials"),
        "inactive": _("This account has been suspended"),
    }

    def confirm_login_allowed(self, user):
        if not user.is_active:
            raise ValidationError(
                "This account is inactive.",
                code="inactive",
            )
