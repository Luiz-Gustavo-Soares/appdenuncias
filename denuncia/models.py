from django.db import models

import uuid

from denuncia.enums import StatusDenuncia, NivelDeRisco, SituacaoAnterior
from denuncia import states as st

from core.models import Endereco




class Denuncia(models.Model):
    data_criacao = models.DateTimeField(auto_now_add=True)
    codigo_denuncia = models.CharField(max_length=40, unique=True, editable=False)

    status = models.CharField(
        choices=StatusDenuncia,
        max_length=2
    )

    risco_automatico = models.CharField(
        choices=NivelDeRisco,
        max_length=2
    )

    @property
    def state(self) -> st.StateDenuncia:
        
        mapping = {
            StatusDenuncia.RASCUNHO: st.RascunhoState,
            StatusDenuncia.SALVO: st.SalvoState,
            StatusDenuncia.VALIDADA: st.ValidadaState,
            StatusDenuncia.ENCAMINHADA: st.EncaminharState,
        }

        return mapping[self.status](self)
    

    def save(self, *args, **kwargs):
        if not self.codigo_denuncia:
            while True:  
                novo_codigo = str(uuid.uuid4())

                if not Denuncia.objects.filter(codigo_denuncia=novo_codigo).exists():
                    self.codigo_denuncia = novo_codigo
                    break
                    
        super().save(*args, **kwargs)

    def __str__(self):
        return f'Denuncia {self.id}'



class DenunciaBaseInfo(models.Model):
    denuncia = models.OneToOneField(
        Denuncia,
        on_delete=models.PROTECT,
        related_name='base_info'
    )

    nome = models.CharField(max_length=100, null=True, blank=True)
    cpf = models.CharField(max_length=20, null=True, blank=True)

    registrou_anteriormente = models.BooleanField()

    situacao_anterior = models.CharField(
        choices=SituacaoAnterior,
        max_length=2,
        null=True,
        blank=True,
    )

    denunciante_envolvida = models.BooleanField()

    endereco_vitima = models.OneToOneField(
        Endereco,
        on_delete=models.PROTECT,
        null=True,
        blank=True,
        related_name='denuncia_v'
    )

    endereco_denunciante = models.OneToOneField(
        Endereco,
        on_delete=models.PROTECT,
        null=True,
        blank=True,
        related_name='denuncia_d'
    )

    def __str__(self):
        return f'Informacoes basicas de {self.denuncia}'