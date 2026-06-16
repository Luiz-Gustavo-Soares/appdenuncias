from django.db import transaction
from django.core.mail import send_mail
from django.urls import reverse
from denuncia.models import Denuncia
from denuncia.enums import StatusDenuncia
from auditoria.services.auditoria_services import validar_revisao

class DenunciaService:
    
    @classmethod
    @transaction.atomic
    def salvar(cls, denuncia: Denuncia):
        denuncia.state.salvar()


    @classmethod
    @transaction.atomic
    def validar(cls, denuncia: Denuncia):
        if validar_revisao(denuncia):
            denuncia.state.validar()


    @classmethod
    @transaction.atomic
    def encaminhar(cls, denuncia: Denuncia):
        denuncia.state.encaminhar()
        cls._enviar_email(denuncia)


    @classmethod
    @transaction.atomic
    def finalizar(cls, denuncia: Denuncia, user):
        CARGO = 'Gerente'
        if not user.groups.filter(name=CARGO).exists():
            raise RuntimeError(f'Usuario nao é um {CARGO}')
        denuncia.state.finalizar()


    
    @classmethod
    def _enviar_email(cls, denuncia):
        url_pdf = reverse(
            "admin:denuncia_pdf",
            args=[denuncia.pk]
        )
        send_mail(
            subject='Envio do caso',
            message=f'Segue o conteudo da denuncia {denuncia}\n Informacoes: http://127.0.0.1:8000{url_pdf}',
            from_email='denuncias@gmail.com',
            recipient_list=['agente@exemplo.com'],
            fail_silently=False,
        )
