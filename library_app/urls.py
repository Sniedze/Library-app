from django.urls import path
from . import views

app_name = 'library_app'

urlpatterns = [

    path('', views.index, name='index'),
    path('borrowed_magazines', views.borrowed_magazines, name='borrowed_magazines'),

    path('catalog', views.catalog, name='catalog'),
    path('magazines', views.magazine_catalog, name='magazines'),
    path('borrow_magazine', views.borrow_magazine, name='borrow_magazine'),
    path('borrow_book', views.borrow_book, name='borrow_book'),
    path('return_book', views.return_book, name='return_book'),
    path('return_magazine', views.return_magazine, name='return_magazine'),
    path('reserve_book', views.reserve_book, name='reserve_book'),
    path('reserve_magazine', views.reserve_magazine, name='reserve_magazine'),
    path('cancel_book_reservation', views.cancel_book_reservation, name='cancel_book_reservation'),
    path('cancel_magazine_reservation', views.cancel_magazine_reservation, name='cancel_magazine_reservation'),
    path('edit_book', views.edit_book, name='edit_book'),
    path('edit_magazine', views.edit_magazine, name='edit_magazine'),

]
