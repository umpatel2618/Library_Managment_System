from django import forms
from .models import *

class AuthorCreateForm(forms.ModelForm):
    class Meta:
        model = Author
        fields = '__all__'
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'au-input au-input--full', 'placeholder': 'First Name'}),
            'last_name': forms.TextInput(attrs={'class': 'au-input au-input--full', 'placeholder': 'Last Name'}),
            'date_of_birth' : forms.DateInput(attrs={'class': 'au-input au-input--full', 'placeholder': 'Date Of Birth'}),
            'date_of_death' : forms.DateInput(attrs={'class': 'au-input au-input--full', 'placeholder': 'Date Of Death'}),
        }

class BookCreateForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = '__all__'
        widgets = {
            'title': forms.TextInput(attrs={'class': 'au-input au-input--full', 'placeholder': 'Book Title'}),
            'author': forms.Select(attrs={'class': 'au-input au-input--full', 'placeholder': 'Select Author'}),
            'summary' : forms.Textarea(attrs={'class': 'au-input au-input--full', 'placeholder': 'Summary Of Book','rows':2,'cols':15}),
            'isbn' : forms.TextInput(attrs={'class': 'au-input au-input--full', 'placeholder': 'Book ISBN Number'}),
            'genre' : forms.Select(attrs={'class': 'au-input au-input--full', 'placeholder': 'Select Genre'}),
        }
class BookInstanceForm(forms.ModelForm):
    class Meta:
        model = BookInstance
        fields = '__all__'
        widgets = {
            'id': forms.TextInput(attrs={'class': 'au-input au-input--full', 'placeholder': 'UUID'}),
            'book': forms.Select(attrs={'class': 'au-input au-input--full', 'placeholder': 'Select Book'}),
            'imprint': forms.TextInput(attrs={'class': 'au-input au-input--full', 'placeholder': 'Book Publication'}),
            'due_back': forms.DateInput(attrs={'class': 'au-input au-input--full', 'placeholder': 'Book Due Date'}),
            'status': forms.Select(attrs={'class': 'au-input au-input--full', 'placeholder': 'Book Status'}),
            'borrower' : forms.Select(attrs={'class': 'au-input au-input--full', 'placeholder': 'Select Borrower'}),
        }
