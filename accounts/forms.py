from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django import forms


class SignUpForm(UserCreationForm):
    pass


class LoginForm(AuthenticationForm):
    pass
