from django.shortcuts import render,redirect,get_object_or_404
from django.views import generic
from .models import *
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import View
from django.http import JsonResponse,HttpResponse
import datetime
from django.contrib.auth.decorators import login_required
from Library_Managment_System.settings import EMAIL_HOST_USER
from django.core.mail import send_mail
from django.utils import timezone
from django.db.models import Q,Count
from django.views.generic.edit import CreateView,UpdateView,DeleteView
from django.urls import reverse_lazy
from .forms import *
import json
# Create your views here.

class BookListView(generic.ListView):
    model = Book
    paginate_by = 5
    context_object_name = 'my_book_list'
    template_name = 'book_managment/book_list.html'

class AuthorListView(generic.ListView):
    model = Author
    context_object_name = 'my_book_list'
    template_name = 'book_managment/author_list.html'


class BookDetailView(generic.DetailView):
    model = Book
    template_name = 'book_managment/book_detail.html'

class LoanedBooksByUserListView(LoginRequiredMixin,generic.ListView):
    model = Transaction
    template_name = "book_managment/bookinstance_list_borrowed_user.html"

    def get_queryset(self):
        return Transaction.objects.filter(borrower=self.request.user).order_by('-bookinstance')


def SearchBook(request):
    """searchbar autocomplete"""
    if request.is_ajax():
        q = request.GET.get('term')
        search_qs = Book.objects.filter(title__istartswith=q)
        results = []
        for r in search_qs:
            results.append(r.title)
        data = json.dumps(results)
    else:
        data = 'fail'
    mimetype = 'application/json'
    return HttpResponse(data, mimetype)

class BookSearch(View):
    """provides list of all book for search """

    def get(self, request):
        return render(request, 'book_managment/book_list.html')

    def post(self, request):
        bookinput = request.POST.get('bookinput').strip()
        searchresult = Book.objects.all().filter(title__iexact=bookinput)
        return render(request, 'book_managment/book_list.html', {'searchresult': searchresult})


class RequestedBook(generic.ListView):
    model = Transaction
    template_name = "book_managment/request_book.html"
    def get_queryset(self):
        if self.request.user.is_staff:
            return self.model.objects.filter(status__in=['r','o'])
        else:
            return self.model.objects.filter(borrower=self.request.user,status__in=['r','o'])

class Pendingrequest(View):
    ''' Pending Request For The Issue Book'''
    def get(self,request,*args, **kwargs):
        transaction = Transaction.objects.all().order_by('requested_date')
        return render(request,'book_managment/pendingrequest.html',{'object_list':transaction})

class Acceptrequest(View):
    ''' Accept Pending Request and issue the Book Status '''
    def get(self,request,*args, **kwargs):
        id  = kwargs['id']
        book = get_object_or_404(BookInstance,id=id) 
        book.due_back = date.today()
        book.due_back = book.due_back + datetime.timedelta(days=7*2)
        book.status = 'o'
        a = BookInstance.objects.filter(id=id).update(status='o')
        Transaction.objects.filter(bookinstance_id = id).update(issue_date=timezone.now(),return_date=None)  
        user = Transaction.objects.all().filter(bookinstance_id=book)[0]
        print(user)
        recepient= user.borrower.email
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
        book.save()
        send_mail(subject,Message,EMAIL_HOST_USER,[recepient],fail_silently=False)
        return HttpResponse(request,'book_managment/pendingrequest.html')

class Deleterequest(View):
    def get(self,request,*args, **kwargs):
        id  = kwargs['id']     
        book = get_object_or_404(BookInstance,id=id)
        if Waiting.objects.filter(book=book):
            print("waiting user delete")
            Waiting.objects.filter(book=book).delete()
        else:
            print("Transaction delete.")
            book.status = 'a'
            book.due_back = None
            book.transaction = None
            book.save()
            Transaction.objects.filter(bookinstance=book).delete()
        return HttpResponse(request,'book_managment/pendingrequest.html')


class BorrowBook(View):
    def get(self,request,*args, **kwargs):
        id = request.GET.get('id',None)
        print(id)
        if id:
            print("inn")
            book = get_object_or_404(BookInstance,id=id)
            total_books = Transaction.objects.all().filter(Q(borrower = request.user) & Q(bookinstance__status='o')).count()

            print(total_books,book)
            if total_books >= 3: 
                return  JsonResponse(status=203,data={'success':True,'msg':"You can not Borrow more than 3 book please return a book"})
            else:    
                
                if book:
                    print("book in")
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
                            return JsonResponse(status=203,data={'success':"This Book is Not Available Yet,So You are added in Waiting List For This book..!"})
                    else: #Issue a New Book
                        print("issue in")
                        Transaction.objects.create(bookinstance=book,borrower=request.user)
                        
                        book.status = 'r'
                        book.save()
                        return JsonResponse(status=200,data={'success':True,'msg':"The Request for issue this Book is sent to librarian.."})
        else:
            print("out")
            return JsonResponse(status=203,data={'fail':False})

class ReturnBook(View):
    def get(self,request,*args, **kwargs):
        id  = kwargs['id']
        print(id)
        if id:
            book = get_object_or_404(BookInstance,id=id).book
            print(book)
            if book:
                result = BookInstance.objects.filter(id=id).update(status='a',due_back=None)
                print(result,"book Become available")
                if Waiting.objects.all().count() > 0: #Assign Book to first user from waiting table
                    print("........................if")
                    user = WaitingTime.objects.filter().first().user
                    
                    
                    BookInstance.objects.filter(id=id).update(status='r')
                    Transaction.objects.create(bookinstance_id=id,borrower=user)
                    recepient = user.email
                    subject = "Your Requested Book is Issued Now"
                    Message = """              -----------Welcome To Library Managment System-----------\n
                                    The Book That You Have requested for is now Available and your request for issue this book have been sent to the librarian.\n
                                    Plaese check more details on website.\n
                                    Thank You..
                                    """
                    Waiting.objects.filter(user=user).delete()
                    print("remove user",user)
                    print(subject,Message,recepient)
                    send_mail(subject,Message,EMAIL_HOST_USER,[recepient],fail_silently=False)
                    print("...assign to first user")
                print("return book")
                book.status = 'a'
                Transaction.objects.filter(bookinstance=id).update(return_date=timezone.now())
                book.save()
                return JsonResponse(status=200,data={'success':True,'msg':"This Book is Returned by You"})
            else:
                return JsonResponse(status=203,data={'fail':False,'msg':"Book is not returned by you."})
        else:
            return JsonResponse(status=203,data={'fail':False})

class Waitinglist(View):
    def get(self,request):
        object_list = WaitingTime.objects.all()
        return render(request,'book_managment/waiting_list.html',{'object_list':object_list})
    
#Author CRUD
class AuthorCreate(CreateView):
    model = Author
    form_class= AuthorCreateForm
    initial = {'date_of_death':'05/01/2018'}
    
class AuthorUpdate(UpdateView):
    model = Author
    form_class= AuthorCreateForm
    template_name = 'book_managment/author_update.html'

class AuthorDelete(DeleteView):
    model = Author
    success_url = reverse_lazy('book_managment:authors')

#Book CRUD
class BookCreateView(CreateView):
    model = Book
    form_class = BookCreateForm
    

class BookUpdateView(UpdateView):
    model = Book
    form_class = BookCreateForm
    template_name = 'book_managment/book_update.html'
    def get_success_url(self):
            return reverse('book_managment:book-detail', kwargs={'pk': self.object.pk})

class BookDeleteView(DeleteView):
    model = Book 
    def get_success_url(self):
            return reverse('book_managment:book-detail', kwargs={'pk': self.object.pk})
    
#BookInstance CRUD
class BookInstanceCreateView(CreateView):
    model = BookInstance
    form_class = BookInstanceForm
    def get_success_url(self):
            return reverse('book_managment:book-detail', kwargs={'pk': self.object.book.pk})

class BookInstanceUpdateView(UpdateView):
    model = BookInstance
    form_class= BookInstanceForm
    template_name = 'book_managment/bookinstance_update.html'
    def get_success_url(self):
            return reverse('book_managment:book-detail', kwargs={'pk': self.object.book.pk})

class BookInstanceDeleteView(DeleteView):
    model = BookInstance 
    def get_success_url(self):
            return reverse('book_managment:book-detail', kwargs={'pk': self.object.book.pk})