from django.db import models
from django.contrib.auth.models import AbstractUser


class CustomUser(AbstractUser):
    name = models.CharField(max_length=150)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=20, blank=True, null = True)
    profile = models.ImageField(upload_to="profiles/", blank=True, null=True) 

    def __str__(self):
        return self.username


