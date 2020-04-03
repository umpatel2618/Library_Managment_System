from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):

    contact = models.CharField(max_length = 12)
    email   = models.EmailField(unique = True)
    city = models.CharField(max_length = 20,null = True,blank=True)
    image = models.ImageField(default='default.png', upload_to='profile_pics',blank=True)
    
    def __str__(self):
        return self.username


    
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    details = models.TextField()

    def __str__(self):
        return self.details

