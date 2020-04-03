from django.urls import path 
from .views import *
from django.conf.urls import url

app_name='book_managment'

urlpatterns = [
    path('books/',BookListView.as_view(),name='books'),
    path('book/<int:pk>/', BookDetailView.as_view(), name='book-detail'),
    path('authors/',AuthorListView.as_view(),name='authors'),
    path('mybooks/',LoanedBooksByUserListView.as_view(),name='my-borrowed'),
    path('borrow/',BorrowBook.as_view(),name='borrow'),
    url(r'ajax_calls/search/$', SearchBook),
    path('searchbook/',BookSearch.as_view(),name='booksearch'),
    # path('<str:id>/return/',ReturnBook.as_view(),name='return'),
    path('waitinglist',Waitinglist.as_view(),name='waiting_list'),

    #Librarian
    path('pendingrequest',Pendingrequest.as_view(),name='pendingrequest'),
    path('<str:id>/acceptrequest',Acceptrequest.as_view(),name='acceptrequest'),
    path('<str:id>/returnrequest',ReturnBook.as_view(),name='returnrequest'),
    path('<str:id>/deleterequest',Deleterequest.as_view(),name='deleterequest'),
    #Author
    path('author/create/',AuthorCreate.as_view(),name='author_create'),
    path('author/<int:pk>/update',AuthorUpdate.as_view(),name='author_update'),
    path('author/<int:pk>/delete',AuthorDelete.as_view(),name='author_delete'),
    #Book
    path('book/create/',BookCreateView.as_view(),name='book_create'),
    path('book/<int:pk>/update',BookUpdateView.as_view(),name='book_update'),
    path('book/<int:pk>/delete',BookDeleteView.as_view(),name='book_delete'),
    
    #BookInstance
    path('bookinstance/create/',BookInstanceCreateView.as_view(),name='bookinstance_create'),
    path('bookinstance/<str:pk>/update/',BookInstanceUpdateView.as_view(),name='bookinstance_update'),
    path('bookinstance/<str:pk>/delete',BookInstanceDeleteView.as_view(),name='bookinstance_delete'),
]
