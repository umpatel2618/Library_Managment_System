from django.shortcuts import render
from django.views import generic
from .models import *
# Create your views here.

class BookListView(generic.ListView):
    model = Book
    context_object_name = 'my_book_list'
    template_name = 'book_managment/book_list.html'

class BookDetailView(generic.DetailView):
    model = Book
    template_name = 'book_managment/book_detail.html'
