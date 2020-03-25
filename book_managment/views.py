from django.shortcuts import render,redirect,get_object_or_404
from django.views import generic
from .models import *
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import View
from django.http import JsonResponse
import datetime
# Create your views here.

class BookListView(generic.ListView):
    model = Book
    context_object_name = 'my_book_list'
    template_name = 'book_managment/book_list.html'

class BookDetailView(generic.DetailView):
    model = Book
    template_name = 'book_managment/book_detail.html'

class LoanedBooksByUserListView(LoginRequiredMixin,generic.ListView):
    model = BookInstance
    template_name = "book_managment/bookinstance_list_borrowed_user.html"

    def get_queryset(self):
        return BookInstance.objects.filter(borrower=self.request.user).filter(status__exact='o').order_by('due_back')

class BorrowBook(View):
    def get(self,request,*args, **kwargs):
        id = request.GET.get('id',None)
        print(id)
        if id:
            book = get_object_or_404(BookInstance,id=id)
            print(book)
            if book:
                book.borrower = request.user
                book.due_back = date.today()
                book.due_back = book.due_back + datetime.timedelta(days=7*2)
                book.status = 'o'
                book.save()
                return JsonResponse(status=200,data={'success':True,'msg':"This Book issue by You"})
            else:
                return JsonResponse(status=203,data={'success':"This Book are not avaliable"})
        else:
            return JsonResponse(status=203,data={'fail':False})
        
