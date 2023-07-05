from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.
class User(AbstractUser):
    name = models.CharField(max_length=200, blank=True, null=True)
    surname = models.CharField(max_length=200, blank=True, null=True)
    email = models.EmailField(unique=True, blank=True, null=True)
    phone_number = models.CharField(max_length=20, blank=True, null=True)
    created = models.DateTimeField(auto_now_add=True)
    last_login = models.DateTimeField(blank=True, null=True, auto_now=True)

    def __str__(self):
        return self.username

class JwtCsrfTokens(models.Model):
    jwt_token = models.CharField(max_length=5000)
    csrf_token = models.CharField(max_length=5000)