from django.db import transaction
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
        pass


    @classmethod
    @transaction.atomic
    def finalizar(cls, denuncia: Denuncia):
        pass
