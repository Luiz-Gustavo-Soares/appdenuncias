from django.contrib import admin
from django.urls import path

from appdenuncias.view import my_view, my_view_parametros


urlpatterns = [
    path('', my_view),
    path('admin/', admin.site.urls),
    path('<str:nome>/', my_view_parametros),
]
