from django.urls import path, include
from django.contrib import admin
from django.views.generic.base import RedirectView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('testing.urls')),
    path('', RedirectView.as_view(url='/accounts/login/', permanent=True), name='home'),
]