from django.contrib.admin import widgets
from django.contrib.auth.forms import UserCreationForm
from django import forms
from .models import *


class RegistrationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('username','contact', 'email','city','password1', 'password2')


        widgets = {
            'username': forms.TextInput(attrs={'class': 'au-input au-input--full', 'placeholder': 'Username'}),
            'contact': forms.TextInput(attrs={'class': 'au-input au-input--full', 'placeholder': 'Contact Number'}),
            'email': forms.EmailInput(attrs={'class': 'au-input au-input--full', 'placeholder': 'Email Address'}),
            'city': forms.TextInput(attrs={'class': 'au-input au-input--full', 'placeholder': 'City'}),
            'password1': forms.PasswordInput(attrs={'class':'au-input au-input--full','placeholder':'Password'}),
            'password2': forms.PasswordInput(attrs={'class': 'au-input au-input--full', 'placeholder': 'Password Again'}),
        }


class LoginForm(forms.Form):
    username = forms.CharField(widget=forms.TextInput(attrs={'class':'au-input au-input--full','placeholder':'Username'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class':'au-input au-input--full','placeholder':'Password'}))

class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('username','contact', 'email','city','image')
        widgets = {
                'username': forms.TextInput(attrs={'class': 'au-input au-input--full', 'placeholder': 'Username'}),
                'contact': forms.TextInput(attrs={'class': 'au-input au-input--full', 'placeholder': 'Contact Number'}),
                'email': forms.EmailInput(attrs={'class': 'au-input au-input--full', 'placeholder': 'Email Address'}),
                'city': forms.TextInput(attrs={'class': 'au-input au-input--full', 'placeholder': 'City'}),
                'image': forms.FileInput(attrs={'class': 'au-input au-input--full', 'placeholder': 'Image'}),

            }
