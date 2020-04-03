from django.db import models
from django.urls import reverse
import uuid  # Required for unique book instances
from accounts.models import User
from datetime import date
from django.utils import timezone
# Create your models here.


class Genre(models.Model):
    """Model representing a book genre."""
    name = models.CharField(max_length=200, help_text="Enter A Book Genre:")

    def __str__(self):
        return self.name


class Book(models.Model):
    """Model representing a book (but not a specific copy of a book)."""
    title = models.CharField(max_length=50)
    author = models.ForeignKey('Author', on_delete=models.SET_NULL, null=True)
    summary = models.TextField(
        max_length=1000, help_text="Enter Brief Description of Book.")
    isbn = models.CharField(
        'ISBN', max_length=13, help_text='13 Character <a href="https://www.isbn-international.org/content/what-isbn">ISBN number</a>')
    genre = models.ManyToManyField(
        Genre, help_text="Select Genre for this book")

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        """Returns the url to access a detail record for this book."""
        return reverse('book_managment:book-detail', args=[str(self.id)])


class BookInstance(models.Model):
    """Model representing a specific copy of a book (i.e. that can be borrowed from the library)."""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4,
                          help_text="Unique ID for this perticular book across whole Library")
    book = models.ForeignKey(Book, on_delete=models.SET_NULL, null=True)
    imprint = models.CharField(max_length=200)
    due_back = models.DateField(null=True, blank=True)
    LOAN_STATUS = (
        ('m', 'Maintenance'),
        ('o', 'On loan'),
        ('a', 'Available'),
        ('r', 'Reserved'),
    )
    status = models.CharField(max_length=1, choices=LOAN_STATUS,
                              blank=True, default='m', help_text="Book Availability")
    
    @property
    def is_overdue(self):
        if self.due_back and date.today() > self.due_back:
            return True
        return False

    class Meta:
        ordering = ['due_back']

    def __str__(self):
        return f'{self.id} ({self.book.title}) ({self.status})'

    def get_absolute_url(self):
        """Returns the url to access a particular author instance."""
        return reverse('book_managment:bookinstance-update', args=[str(self.id)])

class Author(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    date_of_birth = models.DateField(null=True, blank=True)
    date_of_death = models.DateField('Died', null=True, blank=True)

    class Meta:
        ordering = ['last_name', 'first_name']

    def get_absolute_url(self):
        """Returns the url to access a particular author instance."""
        return reverse('book_managment:author-detail', args=[str(self.id)])

    def __str__(self):
        return f'{self.last_name}, {self.first_name}'


class Waiting(models.Model):
    book = models.OneToOneField(BookInstance, on_delete=models.CASCADE)
    user = models.ManyToManyField(User, through="WaitingTime")

    def __str__(self):
        return self.book.book.title


class WaitingTime(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    waiting = models.ForeignKey(Waiting, on_delete=models.CASCADE)
    request_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.request_time)

class Transaction(models.Model):
    bookinstance = models.ForeignKey(BookInstance,on_delete=models.CASCADE)
    borrower = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    requested_date = models.DateTimeField(default=timezone.now)
    issue_date = models.DateTimeField(null=True,blank=True)
    return_date = models.DateTimeField(null=True,blank=True)

    def __str__(self):
        return f'({self.bookinstance.book.title}) ({self.bookinstance.imprint}) ({self.borrower})'
