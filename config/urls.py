from django.contrib import admin
from django.urls import path


admin.site.site_header = 'Администрирование Володи'

urlpatterns = [
    path('admin/', admin.site.urls),
]
