from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.db.models import Q
from django.urls import reverse
from datetime import datetime

from .models import Book
from .models import Magazine
from .models import BorrowedBook
from .models import BorrowedMagazine


@login_required()
def catalog(request):
    books = Book.objects.order_by('title').filter(isAvailable=True)
    context = {
        'books': books,
    }
    return render(request, 'library_app/catalog.html', context)


@login_required()
def magazine_catalog(request):
    magazines = Magazine.objects.order_by('title').filter(isAvailable=True)
    context = {
        'magazines': magazines,
    }
    return render(request, 'library_app/magazines.html', context)


@login_required
def borrow(request):
    borrowed_books = BorrowedBook.objects.filter(user=request.user, isReturned=False)
    if len(borrowed_books) < 10:
        pk = request.POST['pk']
        borrowed_book = get_object_or_404(Book, pk=pk)
        borrowed_book.isAvailable = False
        borrowed_book.save()
        borrow_instance = BorrowedBook()
        borrow_instance.user = request.user
        borrow_instance.book = borrowed_book
        borrow_instance.save()
        return HttpResponseRedirect(reverse('library_app:index'))
    else:
        context = {
            'text1': 'You can not borrow more than 10 books.',
            'text2': 'Please, go to your borrowed book list to return books before borrowing new ones.'

        }
        return render(request, 'library_app/notification.html', context)


@login_required
def borrow_magazine(request):
    borrowed_magazine = BorrowedMagazine.objects.filter(user=request.user, isReturned=False)
    if len(borrowed_magazine) < 3:
        pk = request.POST['pk']
        borrowed_magazine = get_object_or_404(Magazine, pk=pk)
        borrowed_magazine.isAvailable = False
        borrowed_magazine.save()
        borrow_instance = BorrowedMagazine()
        borrow_instance.user = request.user
        borrow_instance.magazine = borrowed_magazine
        borrow_instance.save()
        return HttpResponseRedirect(reverse('library_app:index'))
    else:
        context = {
            'text1': 'You can not borrow more than 3 magazines.',
            'text2': 'Please, go to your borrowed magazine list to return magazines before borrowing new ones.'

        }
        return render(request, 'library_app/notification.html', context)


@login_required
def index(request):
    today = datetime.today()
    user = request.user
    if user.is_superuser:
        overdue_books = BorrowedBook.objects.order_by('-deadline').filter(isReturned=False).filter(
            Q(deadline__gt=today) | Q(deadline=None))
        overdue_magazines = BorrowedMagazine.objects.order_by('-deadline').filter(isReturned=False).filter(
            Q(deadline__gt=today) | Q(deadline=None))
        context = {
            'overdue_books': overdue_books,
            'overdue_magazines': overdue_magazines
        }
        return render(request, 'library_app/overdue.html', context)
    else:
        borrowed_books = BorrowedBook.objects.order_by('borrowed_timestamp').filter(user=request.user, isReturned=False)
        borrowed_magazines = BorrowedMagazine.objects.order_by('borrowed_timestamp').filter(user=request.user,
                                                                                            isReturned=False)
        returned_books = BorrowedBook.objects.order_by('borrowed_timestamp').filter(user=request.user, isReturned=True)
        returned_magazines = BorrowedMagazine.objects.order_by('borrowed_timestamp').filter(user=request.user,
                                                                                            isReturned=True)

        context = {
            'borrowed_books': borrowed_books,
            'returned_books': returned_books,
            'borrowed_magazines': borrowed_magazines,
            'returned_magazines': returned_magazines,
            'user': request.user,
        }

        return render(request, 'library_app/index.html', context)


@login_required()
def return_book(request):
    pk = request.POST['pk']
    fk = request.POST['fk']
    book = get_object_or_404(BorrowedBook, pk=pk)
    book.isReturned = True
    book.save()
    returned_book = get_object_or_404(Book, pk=fk)
    returned_book.isAvailable = True
    returned_book.save()
    return HttpResponseRedirect(reverse('library_app:index'))


@login_required()
def return_magazine(request):
    pk = request.POST['pk']
    fk = request.POST['fk']
    magazine = get_object_or_404(BorrowedMagazine, pk=pk)
    magazine.isReturned = True
    magazine.save()
    returned_magazine = get_object_or_404(Magazine, pk=fk)
    returned_magazine.isAvailable = True
    returned_magazine.save()
    return HttpResponseRedirect(reverse('library_app:index'))
