from django.db import models
from denuncia.enums import NivelDeRisco
from denuncia.models import Denuncia


class AuditoriaAdministrativa(models.Model):

    denuncia = models.OneToOneField(
        Denuncia,
        on_delete=models.PROTECT,
        related_name='auditoria'
    )
    
    observacao = models.TextField(null=True, blank=True)

    nivel_risco_corrigido = models.CharField(
        choices=NivelDeRisco,
        max_length=2
    )