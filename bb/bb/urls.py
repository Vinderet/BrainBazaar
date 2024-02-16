from django.contrib import admin
from django.shortcuts import redirect
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('testing.urls')),
    path('', lambda request: redirect('user_login'), name='home'),
]
