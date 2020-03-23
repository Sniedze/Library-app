from django.contrib import admin
from .models import Book
from .models import BorrowedBook
from .models import Magazine
from .models import BorrowedMagazine

admin.site.register(Book)
admin.site.register(BorrowedBook)
admin.site.register(Magazine)
admin.site.register(BorrowedMagazine)
