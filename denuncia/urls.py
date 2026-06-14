from django.urls import path
from denuncia.views import visualizar_evidencia
from .views import registro, triagem

urlpatterns = [
    path(
        "evidencias/<int:evidencia_id>/",
        visualizar_evidencia,
        name="visualizar_evidencia"
    ),

    path('triagem/', triagem, name='triagem'),
    path('registro/', registro, name='registro'),
]