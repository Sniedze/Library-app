from django.db import models
from django.contrib.auth.models import User
from datetime import datetime, timedelta


class Book(models.Model):
    title = models.CharField(max_length=150)
    author = models.CharField(max_length=150)
    isAvailable = models.BooleanField(default=True)

    def __str__(self):
        return f'{self.title}'


class Magazine(models.Model):
    title = models.CharField(max_length=150)
    isAvailable = models.BooleanField(default=True)

    def __str__(self):
        return f'{self.title}'


def get_deadline():
    return datetime.today() + timedelta(days=30)


class BorrowedBook(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    borrowed_timestamp = models.DateField(default=datetime.today)
    deadline = models.DateField(default=get_deadline)
    isReturned = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.user} - {self.book} - {self.borrowed_timestamp} - {self.deadline}'


def get_magazine_deadline():
    return datetime.today() + timedelta(days=7)


class BorrowedMagazine(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    magazine = models.ForeignKey(Magazine, on_delete=models.CASCADE)
    borrowed_timestamp = models.DateField(default=datetime.today)
    deadline = models.DateField(default=get_magazine_deadline)
    isReturned = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.user} - {self.magazine} - {self.borrowed_timestamp} - {self.deadline}'
