from django.urls import path
from . import views

app_name = 'library_app'

urlpatterns = [

    path('', views.index, name='index'),
    path('catalog', views.catalog, name='catalog'),
    path('magazines', views.magazine_catalog, name='magazine'),
    path('borrow_magazine', views.borrow_magazine, name='borrow_magazine'),
    path('borrow', views.borrow, name='borrow'),
    path('return_book', views.return_book, name='return_book'),
    path('return_magazine', views.return_magazine, name='return_magazine'),

]
