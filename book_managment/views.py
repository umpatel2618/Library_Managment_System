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
from django.utils import timezone
from django.db.models import Q,Count
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
            total_books = BookInstance.objects.filter(borrower=request.user).count()
            print(total_books,book)
            if total_books >= 3: 
                return  JsonResponse(status=203,data={'success':True,'msg':"You can not Borrow more than 3 book please return a book"})
            else:    
                if book:
                    if book.status == 'o': #if book is already borrowed.
                        if Waiting.objects.filter(book=book).exists():
                            if Waiting.objects.filter(~Q(user=request.user)).exists():
                                wait = Waiting.objects.get(book=book)
                                wait.user.add(request.user,through_defaults={'request_time':timezone.now()})
                            else:
                                return JsonResponse(status=203,data={'success':"You are already in waiting list..!"})
                        else:
                            wait = Waiting.objects.create(book=book)
                            wait.user.add(request.user,through_defaults={'request_time':timezone.now()})
                        return JsonResponse(status=203,data={'success':"This Book Not Available Yet,So You are add in Waiting List For This book..!"})
                    else: #Issue a New Book
                        book.borrower = request.user
                        book.due_back = date.today()
                        book.due_back = book.due_back + datetime.timedelta(days=7*2)
                        book.status = 'o'
                        book.save()
                        recepient= request.user.email
                        subject = "Book Issued"
                        Message = """              -----------Welcome To Library Managment System-----------\n
                                    You Are succesfully Issue Book\n
                                    Book Name:"""+ book.book.title + """\n
                                    Book Author:"""+ book.book.author.first_name + "" + book.book.author.last_name+"""\n
                                    Book ISBN Number:"""+ book.book.isbn +"""\n
                                    Book Imprint:"""+ book.imprint +"""\n
                                    Book Return Date:"""+ str(book.due_back) +"""\n
                                    Thank You..
                                    """
                        print(subject,Message,recepient)
                        send_mail(subject,Message,EMAIL_HOST_USER,[recepient],fail_silently=False)
                        return JsonResponse(status=200,data={'success':True,'msg':"This Book issue by You"})
        else:
            return JsonResponse(status=203,data={'fail':False})

class ReturnBook(View):
    def get(self,request,*args, **kwargs):
        id = request.GET.get('id',None)
        print(id)
        if id:
            book = get_object_or_404(BookInstance,id=id).book
            print(book)
            if book:
                result = BookInstance.objects.filter(id=id).update(status='a',borrower=None,due_back=None)
                print(result,"book Become available")
                if Waiting.objects.all().count() > 0: #Assign Book to first user from waiting table
                    print("........................if")
                    user = WaitingTime.objects.filter().first().user
                    Waiting.objects.filter(user=user).delete()
                    print("remove user",user)
                    BookInstance.objects.filter(id=id).update(book=book,due_back= date.today() + datetime.timedelta(days=7*2),status='o',borrower=user)
                    recepient = user.email
                    subject = "Your Requested Book is Issued Now"
                    Message = """              -----------Welcome To Library Managment System-----------\n
                                    The Book That You Have requested for is now succesfully Isuued..\n
                                    Plaese check more details on website.\n
                                    Thank You..
                                    """
                    print(subject,Message,recepient)
                    send_mail(subject,Message,EMAIL_HOST_USER,[recepient],fail_silently=False)
                    print("...assign to first user")
                print("return book")
                book.save()
                return JsonResponse(status=200,data={'success':True,'msg':"This Book is Returned by You"})
            else:
                return JsonResponse(status=203,data={'success':"This Book is not Returned By You"})
        else:
            return JsonResponse(status=203,data={'fail':False})

class Waitinglist(View):
    def post(self,request):
        book_id = request.POST['book']
        print(book_id)  
    def get(self,request):
        object_list = WaitingTime.objects.all()
        return render(request,'book_managment/waiting_list.html',{'object_list':object_list})
    
