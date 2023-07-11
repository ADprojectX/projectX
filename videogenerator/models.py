from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class Request(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    topic = models.CharField(max_length=200)
    voice = models.IntegerField(null = True)
    created = models.DateTimeField(auto_now_add=True)
    script = models.TextField(null=True)

    def __str__(self):
        return f'{self.user.username} - {self.topic}'