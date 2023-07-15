from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    name = models.CharField(max_length=200, blank=True, null=True)
    surname = models.CharField(max_length=200, blank=True, null=True)
    email = models.EmailField(unique=True, blank=True)
    phone_number = models.CharField(max_length=20, blank=True, null=True)
    created = models.DateTimeField(auto_now_add=True)
    last_login = models.DateTimeField(blank=True, null=True, auto_now=True)
    USERNAME_FIELD = 'email'
    # Remove 'email' from REQUIRED_FIELDS
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.email

class JwtCsrfTokens(models.Model):
    jwt_token = models.CharField(max_length=5000)
    csrf_token = models.CharField(max_length=5000)