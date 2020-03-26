from django.shortcuts import render,redirect
from book_managment.models import *
from .forms import *
from django.contrib import messages
from django.urls import reverse
from django.contrib.auth import authenticate, login, logout
from django.views.generic import DetailView, ListView
from django.views.generic import View
# Create your views here.

def home(request):
    # Generate counts of some of the main objects
    num_books = Book.objects.all().count()
    num_instances = BookInstance.objects.all().count()
    # Available books (status = 'a')
    num_instances_available = BookInstance.objects.filter(status__exact='a').count()
    num_authors = Author.objects.count()

    context = {
        'num_books': num_books,
        'num_instances': num_instances,
        'num_instances_available': num_instances_available,
        'num_authors': num_authors,
    }
    return render(request,'accounts/index.html',context=context)

def profile(request):
    return render(request,'accounts/profile.html')

class LogoutView(View):
    def get(self, request):
        logout(request)
        return redirect('accounts:login')


class RegistrationView(View):
    def get(self, request):
        rform = RegistrationForm()
        return render(request, 'accounts/register.html', {'form': rform})

    def post(self, request):
        rform = RegistrationForm(request.POST)
        if rform.is_valid():
            rform.save()
            messages.success(request,"**Registered Succesfully")
            return redirect('accounts:login')
        messages.error(request,"**Please enter valid data.")
        return redirect('accounts:register')


class LoginView(View):

    def get(self, request):
        form1 = LoginForm()
        messages.warning(request, 'Please Login in order to continue!')
        return render(request, 'accounts/login.html', {'form': form1})

    def post(self, request):
        form1 = LoginForm(data=request.POST)
        if form1.is_valid():
            username = form1.cleaned_data.get('username')
            password = form1.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                print('isvalid')
                return redirect('accounts:home')
            else:
                form1 = LoginForm(data=request.POST)
                messages.error(request, 'User Not Found please Enter Valid data' + str(form1.errors))
                return render(request, 'accounts/login.html', {'form': form1})
        else:
            form1 = LoginForm()
            return render(request, 'accounts/login.html', {'form': form1})

