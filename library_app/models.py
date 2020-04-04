from django.db import models
from django.db.models import Q
from django.shortcuts import get_object_or_404

from django.contrib.auth.models import User
from datetime import datetime, timedelta


# #### Abstract model that creates fields in Books and Magazines models #######
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
        return f'{self.title}-{self.author}'


class GetUserArticles(models.Manager):
    # #### Manager method, that gets all user`s borrowed, reserved and returned articles #######
    def get_user_articles(self, status, user):
        articles = self.order_by('borrowed_timestamp').filter(user=user, status=status)
        return articles

    # #### Manager method, that gets catalogs, excluding user`s borrowed and reserved articles #######
    def get_articles(self, user, article_model):
        borrowed_articles = self.order_by('borrowed_timestamp').filter(user=user).filter(
            Q(status='borrowed') | Q(status='reserved'))
        id_list = []
        for borrowed_article in borrowed_articles:
            pk = borrowed_article.article.pk
            id_list.append(pk)
        print(id_list)
        articles = article_model.objects.order_by('title').filter(~Q(pk__in=id_list)).filter(isActive=True)

        return articles


# #### Manager, that includes borrow article method #######
class BorrowArticle(models.Manager):
    def users_articles(self, user):
        borrowed_articles = self.filter(user=user).filter(
            Q(status='borrowed') | Q(status='reserved'))
        return borrowed_articles

    def borrow_article(self, pk, article_model, user):
        borrowed_article = get_object_or_404(article_model, pk=pk)
        borrowed_article.isAvailable = False
        borrowed_article.isReserved = False
        borrowed_article.save()
        borrow_instance = self.get_or_create(user=user, article=borrowed_article, status='borrowed')
        return borrow_instance


class ReserveArticle(models.Manager):
    def users_articles(self, user):
        users_articles = self.filter(user=user).exclude(status="returned")
        return users_articles

    def reserve_article(self, pk, article_model, user):
        reserved_article = get_object_or_404(article_model, pk=pk)
        reserved_article.isAvailable = False
        reserved_article.isReserved = True
        reserved_article.save()
        reserve_instance = self.create(user=user, article=reserved_article, status='reserved')
        return reserve_instance


class ReturnArticle(models.Manager):
    def return_article(self, pk, fk, article_model, borrow_model):
        returned_article = get_object_or_404(article_model, pk=fk)
        return_article = get_object_or_404(borrow_model, pk=pk)
        return_article.status = "returned"
        return_article.save()
        reserved_article = borrow_model.objects.filter(article=returned_article, status='reserved')
        if reserved_article:
            borrow_model.objects.get_or_create(user=reserved_article.user, article=returned_article,
                                               status='borrowed')
            reserved_article.delete()
            returned_article.isAvailable = False
            returned_article.isReserved = False
            returned_article.save()
        else:
            returned_article.isAvailable = True
            returned_article.isReserved = False
            returned_article.save()


def get_deadline():
    return datetime.today() + timedelta(days=30)


# #### Model which contains all borrowed books #######
class BorrowedBook(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    borrowed_timestamp = models.DateField(default=datetime.today)
    article = models.ForeignKey(Book, on_delete=models.CASCADE)
    deadline = models.DateField(default=get_deadline)
    status = models.CharField(default='', max_length=15)

    objects = GetUserArticles()
    borrowed_objects = BorrowArticle()
    reserved_objects = ReserveArticle()
    returned_objects = ReturnArticle()

    def __str__(self):
        return f'{self.user} - {self.article} - {self.borrowed_timestamp} - {self.pk}'


def get_magazine_deadline():
    return datetime.today() + timedelta(days=7)


# #### Model which contains all borrowed magazines #######
class BorrowedMagazine(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    article = models.ForeignKey(Magazine, on_delete=models.CASCADE)
    borrowed_timestamp = models.DateField(default=datetime.today)
    deadline = models.DateField(default=get_magazine_deadline)
    status = models.CharField(default='', max_length=15)

    objects = GetUserArticles()
    borrowed_objects = BorrowArticle()
    reserved_objects = ReserveArticle()
    returned_objects = ReturnArticle()

    def __str__(self):
        return f'{self.user} - {self.article} - {self.borrowed_timestamp} - {self.deadline}'
