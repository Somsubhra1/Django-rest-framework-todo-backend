from django.db import models
from django.contrib.auth.models import User

# Create your models here.


class Task(models.Model):

    title = models.CharField(max_length=200)
    completed = models.BooleanField(default=False, blank=True, null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.title} - {self.user.username}'
