from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.db.models import Q
from django.urls import reverse
from datetime import datetime

from .models import Book, Magazine, BorrowedBook, BorrowedMagazine


@login_required
def index(request):
    today = datetime.today()
    user = request.user
    borrowed_books = BorrowedBook.objects.get_user_articles('borrowed', user)
    overdue_books = BorrowedBook.objects.order_by('-deadline').filter(status='borrowed').filter(
        Q(deadline__gt=today) | Q(deadline=None))
    overdue_magazines = BorrowedMagazine.objects.order_by('-deadline').filter(status='borrowed').filter(
        Q(deadline__gt=today) | Q(deadline=None))
    returned_books = BorrowedBook.objects.get_user_articles('returned', user)
    reserved_books = BorrowedBook.objects.get_user_articles('reserved', user)

    context = {
        'borrowed_books': borrowed_books,
        'returned_books': returned_books,
        'reserved_books': reserved_books,
        'overdue_books': overdue_books,
        'overdue_magazines': overdue_magazines,
        'user': user,
    }
    if user.is_superuser:
        return render(request, 'library_app/overdue.html', context)
    else:
        return render(request, 'library_app/index.html', context)


@login_required
def borrowed_magazines(request):
    user = request.user
    users_magazines = BorrowedMagazine.objects.get_user_articles('borrowed', user)
    returned_magazines = BorrowedMagazine.objects.get_user_articles('returned', user)
    reserved_magazines = BorrowedMagazine.objects.get_user_articles('reserved', user)

    context = {
        'borrowed_magazines': users_magazines,
        'returned_magazines': returned_magazines,
        'reserved_magazines': reserved_magazines,
        'user': user,
    }

    return render(request, 'library_app/borrowed_magazines.html', context)


@login_required()
def catalog(request):
    user = request.user
    articles = BorrowedBook.objects.get_articles(user, Book)
    unavailable_articles = BorrowedBook.objects.order_by('-deadline').filter(status='borrowed')

    context = {
        'books': articles,
        'unavailable_books': unavailable_articles
    }
    if user.is_superuser:
        return render(request, 'library_app/books.html', context)
    else:
        return render(request, 'library_app/catalog.html', context)


@login_required()
def magazine_catalog(request):
    user = request.user
    articles = BorrowedMagazine.objects.get_articles(user, Magazine)
    unavailable_articles = BorrowedMagazine.objects.order_by('-deadline').filter(status='borrowed')

    context = {
        'magazines': articles,
        'unavailable_magazines': unavailable_articles
    }
    user = request.user
    if user.is_superuser:
        return render(request, 'library_app/press.html', context)
    else:
        return render(request, 'library_app/magazines.html', context)


@login_required
def borrow_book(request):
    user = request.user
    pk = request.POST['pk']
    borrowed_books = BorrowedBook.borrowed_objects.users_articles(user)
    if borrowed_books.count() < 10:
        BorrowedBook.borrowed_objects.borrow_article(pk, Book, user)
        return HttpResponseRedirect(reverse('library_app:index'))
    else:
        context = {
            'text1': 'You can not borrow more than 10 books.',
            'text2': 'Please, go to your borrowed book list to return books before borrowing new ones.',
            'template': '',

        }
        return render(request, 'library_app/notification.html', context)


@login_required
def borrow_magazine(request):
    user = request.user
    pk = request.POST['pk']
    borrowed_articles = BorrowedMagazine.borrowed_objects.users_articles(user)
    if borrowed_articles.count() < 3:
        BorrowedMagazine.borrowed_objects.borrow_article(pk, Magazine, user)
        return HttpResponseRedirect(reverse('library_app:borrowed_magazines'))
    else:
        context = {
            'text1': 'You can not borrow more than 3 magazines.',
            'text2': 'Please, go to your borrowed magazine list to return magazines before borrowing new ones.',
            'template': "borrowed_magazines",

        }
        return render(request, 'library_app/notification.html', context)


@login_required
def reserve_book(request):
    user = request.user
    pk = request.POST['pk']
    users_books = BorrowedBook.reserved_objects.users_articles(user)
    if users_books.count() < 10:
        BorrowedBook.reserved_objects.reserve_article(pk, Book, user)
        return HttpResponseRedirect(reverse('library_app:index'))
    else:
        context = {
            'text1': 'You can not borrow more than 3 books.',
            'text2': 'Please, go to your borrowed book list to return books before borrowing new ones.'
        }
        return render(request, 'library_app/notification.html', context)


@login_required
def reserve_magazine(request):
    user = request.user
    pk = request.POST['pk']
    users_magazines = BorrowedMagazine.reserved_objects.users_articles(user)
    if users_magazines.count() < 3:
        BorrowedMagazine.reserved_objects.reserve_article(pk, Magazine, user)
        return HttpResponseRedirect(reverse('library_app:borrowed_magazines'))
    else:
        context = {
            'text1': 'You can not borrow more than 3 magazines.',
            'text2': 'Please, go to your borrowed magazine list to return magazines before borrowing new ones.'
        }
        return render(request, 'library_app/notification.html', context)


@login_required()
def return_book(request):
    pk = request.POST['pk']
    fk = request.POST['fk']
    BorrowedBook.returned_objects.return_article(pk, fk, Book, BorrowedBook)
    return HttpResponseRedirect(reverse('library_app:index'))


@login_required()
def return_magazine(request):
    pk = request.POST['pk']
    fk = request.POST['fk']
    BorrowedMagazine.returned_objects.return_article(pk, fk, Magazine, BorrowedMagazine)
    return HttpResponseRedirect(reverse('library_app:borrowed_magazines'))


@login_required
def edit_book(request):
    pk = request.POST['pk']
    del_book = get_object_or_404(Book, pk=pk)
    del_book.isActive = False
    del_book.save()

    return HttpResponseRedirect(reverse('library_app:catalog'))


@login_required
def edit_magazine(request):
    pk = request.POST['pk']
    del_magazine = get_object_or_404(Magazine, pk=pk)
    del_magazine.isActive = False
    del_magazine.save()
    return HttpResponseRedirect(reverse('library_app:magazines'))


@login_required
def cancel_book_reservation(request):
    pk = request.POST['pk']
    fk = request.POST['fk']
    book = get_object_or_404(Book, pk=fk)
    book.isReserved = False
    book.isAvailable = False
    book.save()
    reserved_book = get_object_or_404(BorrowedBook, pk=pk)
    reserved_book.delete()
    return HttpResponseRedirect(reverse('library_app:index'))


@login_required
def cancel_magazine_reservation(request):
    pk = request.POST['pk']
    fk = request.POST['fk']
    magazine = get_object_or_404(Magazine, pk=fk)
    magazine.isReserved = False
    magazine.isAvailable = False
    magazine.save()
    reserved_magazine = get_object_or_404(BorrowedMagazine, pk=pk)
    reserved_magazine.delete()
    return HttpResponseRedirect(reverse('library_app:index'))
