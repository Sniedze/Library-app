from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('library_app.urls')),
    path('accounts/', include('login_app.urls')),
]
