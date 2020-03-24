from django.contrib.admin import widgets
from django.contrib.auth.forms import UserCreationForm
from django import forms
from .models import *


class RegistrationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('username','contact', 'email', 'password1', 'password2')


class LoginForm(forms.Form):
    username = forms.CharField(max_length=10, label="Enter Username")
    password = forms.CharField(max_length=20, label="Enter Password", widget=forms.PasswordInput())
