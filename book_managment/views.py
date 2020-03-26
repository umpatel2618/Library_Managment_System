from django.shortcuts import render,redirect,get_object_or_404
from django.views import generic
from .models import *
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import View
from django.http import JsonResponse
import datetime
from django.contrib.auth.decorators import login_required
from Library_Managment_System.settings import EMAIL_HOST_USER
from django.core.mail import send_mail
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
            a = BookInstance.objects.filter(borrower=request.user).count()
            print(a,book)
            if a >= 3:
                return  JsonResponse(status=203,data={'success':True,'msg':"You can not Borrow more than 3 book please return a book"})
            elif book.status == 'o':
                return  JsonResponse(status=203,data={'success':True,'msg':"This Book Is Already On Loan, wait untill its become available"})
                if book:
                    book.borrower = request.user
                    book.due_back = date.today()
                    book.due_back = book.due_back + datetime.timedelta(days=7*2)
                    book.status = 'o'
                    
                    recepient= request.user.email
                    subject = "Book Issued"
                    Message = """-----------Welcome To Library Managment System-----------\n
                                 You Are succesfully Issue Book\n
                                 Book Name:"""+ book.book + """\n
                                 Book Author:"""+ book.author +"""\n
                                 Book ISBN Number:"""+ book.isbn +"""\n
                                 Book Imprint:"""+ book.imprint +"""\n
                                 Book Return Date:"""+ book.due_back +"""\n
                                 Thank You..
                                """
                    send_mail(subject,Message,EMAIL_HOST_USER,[recepient],fail_silently=False)
                    book.save()
                    return JsonResponse(status=200,data={'success':True,'msg':"This Book issue by You"})
                else:
                    return JsonResponse(status=203,data={'success':"This Book are not avaliable"})
        else:
            return JsonResponse(status=203,data={'fail':False})

        
        

class ReturnBook(View):
    def get(self,request,*args, **kwargs):
        id = request.GET.get('id',None)
        print(id)
        if id:
            book = get_object_or_404(BookInstance,id=id)
            if book:
                book.borrower = None
                book.due_back = None
                book.status = 'a'
                book.save()
                return JsonResponse(status=200,data={'success':True,'msg':"This Book is Returned by You"})
                return redirect('book_managment:mybooks')
            else:
                return JsonResponse(status=203,data={'success':"This Book is not Returned By You"})
        else:
            return JsonResponse(status=203,data={'fail':False})
