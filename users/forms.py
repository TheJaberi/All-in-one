from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator
from django.db import transaction

from .models import User, Company, Customer

class DateInput(forms.DateInput):
    input_type = 'date'

def validate_email(value):
    if User.objects.filter(email=value).exists():
        raise ValidationError(f"{value} is already taken.")

class CustomerSignUpForm(UserCreationForm):
    username = forms.CharField(
        max_length=30,
        label="Username",
        widget= forms.TextInput(attrs={'placeholder': 'Enter username'}),
        help_text="Enter your desired username. Max 30 characters."
    )
    email = forms.EmailField(
        validators=[validate_email],
        widget= forms.TextInput(attrs={'placeholder': 'Enter email'}),
        label="Email",
        help_text="Enter a valid email address. This will be used for account verification."
    )
    date_of_birth = forms.DateField(
        widget=DateInput(attrs={'placeholder': 'dd/mm/yyyy'}),
        label="Date of Birth",
        help_text="Enter your date of birth in the format DD/MM/YYYY."
    )
    password1 = forms.CharField(
        widget=forms.PasswordInput(attrs={'placeholder': 'Enter password'}),
        label="Password",
        help_text="Enter a strong password. It should be at least 8 characters long and contain letters and numbers.",
        validators=[RegexValidator(
            regex='^(?=.*[a-zA-Z])(?=.*\d)',
            message='Password must contain at least one letter and one number.'
        )]
    )
    password2 = forms.CharField(
        widget=forms.PasswordInput(attrs={'placeholder': 'Confirm password'}),
        label="Confirm Password",
        help_text="Enter the same password again for confirmation."
    )

    class Meta(UserCreationForm.Meta):
        model = User
        fields = ('username', 'email', 'date_of_birth', 'password1', 'password2')

    @transaction.atomic
    def save(self):
        user = super().save(commit=False)
        user.is_customer = True
        user.save()
        Customer.objects.create(user=user, birth=self.cleaned_data.get('date_of_birth'))
        return user

class CompanySignUpForm(UserCreationForm):
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
    field_of_work = forms.ChoiceField(
        choices=[
            ('Air Conditioner', 'Air Conditioner'),
            ('All in One', 'All in One'),
            ('Carpentry', 'Carpentry'),
            ('Electricity', 'Electricity'),
            ('Gardening', 'Gardening'),
            ('Home Machines', 'Home Machines'),
            ('Housekeeping', 'Housekeeping'),
            ('Interior Design', 'Interior Design'),
            ('Locks', 'Locks'),
            ('Painting', 'Painting'),
            ('Plumbing', 'Plumbing'),
            ('Water Heaters', 'Water Heaters'),
        ],
        label="Field of Work",
        help_text="Select the field of work of your company."
    )
    password1 = forms.CharField(
        widget=forms.PasswordInput,
        label="Password",
        help_text="Enter a strong password. It should be at least 8 characters long and contain letters and numbers.",
        validators=[RegexValidator(
            regex='^(?=.*[a-zA-Z])(?=.*\d)',
            message='Password must contain at least one letter and one number.'
        )]
    )
    password2 = forms.CharField(
        widget=forms.PasswordInput,
        label="Confirm Password",
        help_text="Enter the same password again for confirmation."
    )

    class Meta(UserCreationForm.Meta):
        model = User
        fields = ('username', 'email', 'field_of_work', 'password1', 'password2')

    @transaction.atomic
    def save(self):
        user = super().save(commit=False)
        user.is_company = True
        user.save()
        Company.objects.create(user=user, field=self.cleaned_data.get('field_of_work'))
        return user

class UserLoginForm(forms.Form):
    email = forms.CharField(widget=forms.TextInput(
        attrs={'placeholder': 'Enter Email or password'}))
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'placeholder': 'Enter Password'}))

    def __init__(self, *args, **kwargs):
        super(UserLoginForm, self).__init__(*args, **kwargs)
        self.fields['email'].widget.attrs['autocomplete'] = 'off'
