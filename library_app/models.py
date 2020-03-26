from django.db import models
from django.contrib.auth.models import User
from datetime import datetime, timedelta


class CatalogCreationModel(models.Model):
    title = models.CharField(max_length=150)
    author = models.CharField(max_length=150, blank=True)
    isAvailable = models.BooleanField(default=True)
    isReserved = models.BooleanField(default=False)
    isActive = models.BooleanField(default=True)

    class Meta:
        abstract = True


class Magazine(CatalogCreationModel):

    def __str__(self):
        return f'{self.title}'


class Book(CatalogCreationModel):

    def __str__(self):
        return f'{self.title}'


class GetArticle(models.Manager):
    def get_articles(self, status, user):
        articles = self.order_by('borrowed_timestamp').filter(user=user, status=status)
        return articles


def get_deadline():
    return datetime.today() + timedelta(days=30)


class BorrowedBook(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    borrowed_timestamp = models.DateField(default=datetime.today)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    deadline = models.DateField(default=get_deadline)
    status = models.CharField(default='', max_length=15)

    objects = GetArticle()

    def __str__(self):
        return f'{self.user} - {self.book} - {self.borrowed_timestamp} - {self.deadline}'


def get_magazine_deadline():
    return datetime.today() + timedelta(days=7)


class BorrowedMagazine(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    magazine = models.ForeignKey(Magazine, on_delete=models.CASCADE)
    borrowed_timestamp = models.DateField(default=datetime.today)
    deadline = models.DateField(default=get_magazine_deadline)
    status = models.CharField(default='', max_length=15)

    objects = GetArticle()

    def __str__(self):
        return f'{self.user} - {self.magazine} - {self.borrowed_timestamp} - {self.deadline}'
