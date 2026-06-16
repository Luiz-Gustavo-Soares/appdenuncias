from django.db import models
from django.utils.html import format_html
from django.urls import reverse

import uuid

from denuncia.enums import StatusDenuncia
from denuncia import states as st

from core.models import Endereco


class Denuncia(models.Model):
    data_criacao = models.DateTimeField(auto_now_add=True)
    codigo_denuncia = models.CharField(max_length=40, unique=True, editable=False)

    status = models.CharField(
        choices=StatusDenuncia,
        max_length=2,
        default=StatusDenuncia.RASCUNHO

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

    perigo_imediato = models.BooleanField()
    registrou_anteriormente = models.BooleanField()

    situacao_anterior = models.CharField(max_length=80,null=True,blank=True,)

    denunciante_envolvida = models.BooleanField()

    endereco = models.OneToOneField(
        Endereco,
        on_delete=models.PROTECT,
        null=True,
        blank=True,
        related_name='denuncia'
    )

    def __str__(self):
        return f'Informacoes basicas de {self.denuncia}'
    

def upload_evidencia(instance, filename):

    return (
        f"evidencias/"
        f"denuncia_{instance.denuncia_id}/"
        f"{str(uuid.uuid4())[:8]}-{filename}"
    )

class Evidencia(models.Model):

    denuncia = models.ForeignKey(
        "Denuncia",
        on_delete=models.CASCADE,
        related_name="evidencias"
    )

    arquivo = models.FileField(
        upload_to=upload_evidencia
    )

    data_upload = models.DateTimeField(
        auto_now_add=True
    )


    def get_url(self):
        return reverse(
                    "denuncia:visualizar_evidencia",
                    args=[self.id]
                )


    def download(self):

        if self.arquivo:

            return format_html(
                '<a href="{}">Baixar</a>',
                self.get_url()
            )

        return "-"