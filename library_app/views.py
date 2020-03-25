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


@login_required
def index(request):
    today = datetime.today()
    user = request.user
    if user.is_superuser:
        overdue_books = BorrowedBook.objects.order_by('-deadline').filter(status='borrowed').filter(
            Q(deadline__gt=today) | Q(deadline=None))
        overdue_magazines = BorrowedMagazine.objects.order_by('-deadline').filter(status='borrowed').filter(
            Q(deadline__gt=today) | Q(deadline=None))
        context = {
            'overdue_books': overdue_books,
            'overdue_magazines': overdue_magazines
        }
        return render(request, 'library_app/overdue.html', context)
    else:
        borrowed_books = BorrowedBook.objects.order_by('borrowed_timestamp').filter(user=request.user,
                                                                                    status='borrowed')
        borrowed_magazines = BorrowedMagazine.objects.order_by('borrowed_timestamp').filter(user=request.user,
                                                                                            status='borrowed')
        returned_books = BorrowedBook.objects.order_by('-borrowed_timestamp').filter(user=request.user,
                                                                                     status='returned')
        returned_magazines = BorrowedMagazine.objects.order_by('-borrowed_timestamp').filter(user=request.user,
                                                                                             status='returned')
        reserved_books = BorrowedBook.objects.filter(user=request.user,
                                                     status='reserved')
        reserved_magazines = BorrowedMagazine.objects.filter(user=request.user,
                                                             status='reserved')

        context = {
            'borrowed_books': borrowed_books,
            'returned_books': returned_books,
            'reserved_books': reserved_books,
            'borrowed_magazines': borrowed_magazines,
            'returned_magazines': returned_magazines,
            'reserved_magazines': reserved_magazines,
            'user': request.user,
        }
        return render(request, 'library_app/index.html', context)


@login_required()
def catalog(request):
    borrowed_books = BorrowedBook.objects.order_by('borrowed_timestamp').filter(user=request.user).filter(
        Q(status='borrowed') | Q(status='reserved'))
    id_list = []
    for borrowed_book in borrowed_books:
        pk = borrowed_book.book.pk
        id_list.append(pk)
    print(id_list)
    books = Book.objects.order_by('title').filter(~Q(pk__in=id_list))
    unavailable_books = BorrowedBook.objects.order_by('-deadline').filter(status='borrowed')

    context = {
        'books': books,
        'unavailable_books': unavailable_books
    }
    user = request.user
    if user.is_superuser:
        return render(request, 'library_app/books.html', context)
    else:
        return render(request, 'library_app/catalog.html', context)


@login_required()
def magazine_catalog(request):
    borrowed_magazines = BorrowedMagazine.objects.order_by('borrowed_timestamp').filter(user=request.user).filter(
        Q(status='borrowed') | Q(status='reserved'))
    id_list = []
    for borrowed_magazine in borrowed_magazines:
        pk = borrowed_magazine.magazine.pk
        id_list.append(pk)
    print(id_list)
    magazines = Magazine.objects.order_by('title').filter(~Q(pk__in=id_list))
    unavailable_magazines = BorrowedMagazine.objects.order_by('-deadline').filter(status='borrowed')
    context = {
        'magazines': magazines,
        'unavailable_magazines': unavailable_magazines,
    }
    user = request.user
    if user.is_superuser:
        return render(request, 'library_app/press.html', context)
    else:
        return render(request, 'library_app/magazines.html', context)


@login_required
def borrow_book(request):
    borrowed_books = BorrowedBook.objects.filter(user=request.user, status='borrowed')
    if len(borrowed_books) < 10:
        pk = request.POST['pk']
        borrowed_book = get_object_or_404(Book, pk=pk)
        borrowed_book.isAvailable = False
        borrowed_book.isReserved = False
        borrowed_book.save()
        borrow_instance = BorrowedBook()
        borrow_instance.user = request.user
        borrow_instance.book = borrowed_book
        borrow_instance.status = 'borrowed'
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
    borrowed_magazine = BorrowedMagazine.objects.filter(user=request.user, status='borrowed')
    if len(borrowed_magazine) < 3:
        pk = request.POST['pk']
        borrowed_magazine = get_object_or_404(Magazine, pk=pk)
        borrowed_magazine.isAvailable = False
        borrowed_magazine.isReserved = False
        borrowed_magazine.save()
        borrow_instance = BorrowedMagazine()
        borrow_instance.user = request.user
        borrow_instance.magazine = borrowed_magazine
        borrow_instance.status = 'borrowed'
        borrow_instance.save()
        return HttpResponseRedirect(reverse('library_app:index'))
    else:
        context = {
            'text1': 'You can not borrow more than 3 magazines.',
            'text2': 'Please, go to your borrowed magazine list to return magazines before borrowing new ones.'

        }
        return render(request, 'library_app/notification.html', context)


@login_required
def reserve_book(request):
    borrowed_book = BorrowedBook.objects.filter(user=request.user).exclude(status="returned")
    if len(borrowed_book) < 10:
        pk = request.POST['pk']
        reserved_book = get_object_or_404(Book, pk=pk)
        reserved_book.isReserved = True
        reserved_book.isAvailable = False
        reserved_book.save()
        book_instance = BorrowedBook()
        book_instance.user = request.user
        book_instance.book = reserved_book
        book_instance.status = 'reserved'
        book_instance.save()
        return HttpResponseRedirect(reverse('library_app:index'))
    else:
        context = {
            'text1': 'You can not borrow more than 3 books.',
            'text2': 'Please, go to your borrowed book list to return magazines before borrowing new ones.'
        }
        return render(request, 'library_app/notification.html', context)


@login_required
def reserve_magazine(request):
    borrowed_magazine = BorrowedMagazine.objects.filter(user=request.user).exclude(status="returned")

    if len(borrowed_magazine) < 3:
        pk = request.POST['pk']
        reserved_magazine = get_object_or_404(Magazine, pk=pk)
        reserved_magazine.isReserved = True
        reserved_magazine.isAvailable = False
        reserved_magazine.save()
        magazine_instance = BorrowedMagazine()
        magazine_instance.user = request.user
        magazine_instance.magazine = reserved_magazine
        magazine_instance.status = 'reserved'
        magazine_instance.save()
        return HttpResponseRedirect(reverse('library_app:index'))
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
    book = get_object_or_404(BorrowedBook, pk=pk)
    book.status = "returned"
    book.save()
    returned_book = get_object_or_404(Book, pk=fk)
    returned_book.isAvailable = True
    returned_book.isReserved = False
    returned_book.save()
    return HttpResponseRedirect(reverse('library_app:index'))


@login_required()
def return_magazine(request):
    pk = request.POST['pk']
    fk = request.POST['fk']
    magazine = get_object_or_404(BorrowedMagazine, pk=pk)
    magazine.status = "returned"
    magazine.save()
    returned_magazine = get_object_or_404(Magazine, pk=fk)
    returned_magazine.isAvailable = True
    returned_magazine.isReserved = False
    returned_magazine.save()
    return HttpResponseRedirect(reverse('library_app:index'))


@login_required
def edit_book(request):
    pk = request.POST['pk']
    del_book = get_object_or_404(Book, pk=pk)
    del_book.delete()

    return render(request, 'library_app/book.html')


@login_required
def edit_magazine(request):
    pk = request.POST['pk']
    del_magazine = get_object_or_404(Magazine, pk=pk)
    del_magazine.delete()

    return render(request, 'library_app/press.html')


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
