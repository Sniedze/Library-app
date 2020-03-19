from django.shortcuts import render, get_object_or_404
from .models import Book


def index(request):
    books = Book.objects.order_by('title').filter(isAvailable=True)
    context = {
        'books': books,
    }
    return render(request, 'library_app/index.html', context)
