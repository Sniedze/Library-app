from django.db import models
from django.contrib.auth.models import User


class Book(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    title = models.CharField(max_length=150)
    author = models.CharField(max_length=150)
    isAvailable = models.BooleanField(default=True)

    def __str__(self):
        return self.title
