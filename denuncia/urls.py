from django.urls import path
from denuncia.views import visualizar_evidencia

urlpatterns = [
    path(
        "evidencias/<int:evidencia_id>/",
        visualizar_evidencia,
        name="visualizar_evidencia"
    )
]