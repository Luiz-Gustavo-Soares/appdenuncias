from django.contrib import admin
from django.urls import path

from appdenuncias.view import my_view, my_view_parametros


urlpatterns = [
    path('', my_view),
    path('<str:nome>/', my_view_parametros),
    path('admin/', admin.site.urls),
]
