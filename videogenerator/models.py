from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class Request(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    topic = models.CharField(max_length=200)
    voice = models.CharField(max_length=200, null=True)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.user.username} - {self.topic}'


class Script(models.Model):
    request = models.OneToOneField(Request, on_delete=models.CASCADE, primary_key=True)
    script_data = models.JSONField()

    class Meta:
        # Define a unique_together constraint to prevent duplicates based on the 'request_id' field
        unique_together = ['request_id']

class PendingTask(models.Model):
    request = models.OneToOneField(Request, on_delete=models.CASCADE, primary_key=True)
    prompt = models.TextField(null=True)
    folder = models.TextField(null=True)