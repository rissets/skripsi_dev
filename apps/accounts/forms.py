from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


class RegisterForm(UserCreationForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ["username", "email", "password1", "password2"]
        widgets = {
            "username": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Username",
                    "required": True,
                }
            ),
            "email": forms.EmailInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Email",
                    "required": True,
                }
            ),
            "password1": forms.PasswordInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Password",
                    "required": True,
                }
            ),
            "password2": forms.PasswordInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Confirm Password",
                    "required": True,
                }
            ),
        }