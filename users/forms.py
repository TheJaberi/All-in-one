from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, authenticate
from django.db import transaction
from django.core.exceptions import ValidationError

from .models import User, Company, Customer


class DateInput(forms.DateInput):
    input_type = 'date'


def validate_email(value):
    # In case the email already exists in an email input in a registration form, this function is fired
    if User.objects.filter(email=value).exists():
        raise ValidationError(
            value + " is already taken.")


class CustomerSignUpForm(UserCreationForm):
    username = forms.CharField(
        max_length=30,
        label="Username",
        help_text="Enter your desired username. Max 30 characters."
    )
    email = forms.EmailField(
        validators=[validate_email],
        label="Email",
        help_text="Enter a valid email address. This will be used for account verification."
    )
    date_of_birth = forms.DateField(
        widget=DateInput(attrs={'placeholder': 'dd/mm/yyyy'}),
        label="Date of Birth",
        help_text="Enter your date of birth in the format DD/MM/YYYY."
    )
    password1 = forms.CharField(
        widget=forms.PasswordInput,
        label="Password",
        help_text="Enter a strong password. It should be at least 8 characters long."
    )
    password2 = forms.CharField(
        widget=forms.PasswordInput,
        label="Confirm Password",
        help_text="Enter the same password again for confirmation."
    )


class CompanySignUpForm(UserCreationForm):
    pass


class UserLoginForm(forms.Form):
    def __init__(self, *args, **kwargs):
        super(UserLoginForm, self).__init__(*args, **kwargs)

    email = forms.EmailField(widget=forms.TextInput(
        attrs={'placeholder': 'Enter Email'}))
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'placeholder': 'Enter Password'}))

    def __init__(self, *args, **kwargs):
        super(UserLoginForm, self).__init__(*args, **kwargs)
        self.fields['email'].widget.attrs['autocomplete'] = 'off'
