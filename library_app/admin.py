from django.contrib import admin
from .models import Book
from .models import BorrowedBook

admin.site.register(Book)
admin.site.register(BorrowedBook)
