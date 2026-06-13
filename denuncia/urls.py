from django.urls import path
from .views import registro, triagem

app_name = 'denuncia'

urlpatterns = [
    path('triagem/', triagem, name='triagem'),
    path('registro/', registro, name='registro'),
]