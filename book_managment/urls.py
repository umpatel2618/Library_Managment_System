from django.urls import path 
from .views import *

app_name='book_managment'

urlpatterns = [
    path('books/',BookListView.as_view(),name='books'),
    path('book/<int:pk>/', BookDetailView.as_view(), name='book-detail'),
    path('mybooks/',LoanedBooksByUserListView.as_view(),name='my-borrowed'),
    path('borrow/',BorrowBook.as_view(),name='borrow'),
    path('return/',ReturnBook.as_view(),name='return'),
    path('waitinglist',Waitinglist.as_view(),name='waiting_list'),
]
