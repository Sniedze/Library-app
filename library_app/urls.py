from django.urls import path
from . import views

app_name = 'library_app'

urlpatterns = [

    path('', views.index, name='index'),
    path('catalog', views.catalog, name='catalog'),
    path('borrow', views.borrow, name='borrow'),
    path('return_book', views.return_book, name='return_book')

]
