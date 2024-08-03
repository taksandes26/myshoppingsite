from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django import forms
from .models import Address


class SignUpForm(UserCreationForm):
    pass


class LoginForm(AuthenticationForm):
    pass


class AddressForm(forms.ModelForm):
    class Meta:
        model = Address
        fields = ['type', 'city', 'country', 'pincode']
