
from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth.models import AbstractUser

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    email = models.EmailField( max_length=254, unique=True)  
    def __str__(self):
        return f"{self.user.username}'s Profile"


