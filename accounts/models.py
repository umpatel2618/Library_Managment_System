from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):

    contact = models.CharField(max_length = 12)
    email   = models.EmailField(unique = True)

    def __str__(self):
        return self.first_name

    
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    details = models.TextField()

    def __str__(self):
        return self.details

