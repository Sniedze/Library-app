from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.db.models import Q

from django.urls import reverse
from datetime import datetime, timedelta

from .models import Book
from .models import BorrowedBook


def catalog(request):
    books = Book.objects.order_by('title').filter(isAvailable=True)
    context = {
        'books': books,
    }
    return render(request, 'library_app/catalog.html', context)


@login_required
def borrow(request):
    pk = request.POST['pk']
    print(pk)
    borrowed_book = get_object_or_404(Book, pk=pk)
    borrowed_book.isAvailable = False
    borrowed_book.save()
    borrow_instance = BorrowedBook()
    borrow_instance.user = request.user
    borrow_instance.book = borrowed_book
    borrow_instance.save()
    return HttpResponseRedirect(reverse('library_app:catalog'))


@login_required
def index(request):
    borrowed_books = BorrowedBook.objects.filter(user=request.user, isReturned=False)
    returned_books = BorrowedBook.objects.filter(user=request.user, isReturned=True)

    context = {
        'borrowed_books': borrowed_books,
        'returned_books': returned_books,
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
def librarian(request):
    user = request.user
    today = datetime.today()
    if user.is_superuser:
        books_over_deadline = BorrowedBook.objects.order_by('-date').filter(isReturned=False).filter(
            Q(valid_until__gte=today) | Q(valid_until=None))
        context = {
            'books_over_deadline': books_over_deadline
        }
        return render(request, 'library_app/overdue.html', context)
