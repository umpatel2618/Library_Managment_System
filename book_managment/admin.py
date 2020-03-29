from django.contrib import admin
from .models import *

# Register your models here.
admin.site.register(Book)
admin.site.register(Genre)
admin.site.register(Author)
admin.site.register(BookInstance)
admin.site.register(Waiting)
admin.site.register(WaitingTime)
