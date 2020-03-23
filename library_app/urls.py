from django.urls import path
from . import views

app_name = 'library_app'

urlpatterns = [

    path('', views.index, name='index'),
    path('catalog', views.catalog, name='catalog'),
    path('magazines', views.magazine_catalog, name='magazine'),
    path('borrow_magazine', views.borrow_magazine, name='borrow_magazine'),
    path('borrow_book', views.borrow_book, name='borrow_book'),
    path('return_book', views.return_book, name='return_book'),
    path('return_magazine', views.return_magazine, name='return_magazine'),
    path('edit_book', views.edit_book, name='edit_book'),
    path('edit_magazine', views.edit_magazine, name='edit_magazine'),

]
