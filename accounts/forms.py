from django.contrib.admin import widgets
from django.contrib.auth.forms import UserCreationForm
from django import forms
from .models import *


class RegistrationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('username','contact', 'email', 'password1', 'password2')


        widgets = {
            'username': forms.TextInput(attrs={'class': 'au-input au-input--full', 'placeholder': 'Username'}),
            'contact': forms.TextInput(attrs={'class': 'au-input au-input--full', 'placeholder': 'Contact Number'}),
            'email': forms.EmailInput(attrs={'class': 'au-input au-input--full', 'placeholder': 'Email Address'}),
            'password1': forms.PasswordInput(attrs={'class':'au-input au-input--full','placeholder':'Password'}),
            'password2': forms.PasswordInput(attrs={'class': 'au-input au-input--full', 'placeholder': 'Password Again'}),
        }


class LoginForm(forms.Form):
    username = forms.CharField(widget=forms.TextInput(attrs={'class':'au-input au-input--full','placeholder':'Username'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class':'au-input au-input--full','placeholder':'Password'}))
