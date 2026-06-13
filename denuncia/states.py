from abc import ABC
from denuncia.enums import StatusDenuncia


class StateDenuncia(ABC):
    def __init__(self, denuncia):
        self.denuncia = denuncia

    def salvar(self):
        raise RuntimeError("Operação inválida")

    def validar(self):
        raise RuntimeError("Operação inválida")

    def salvar(self):
        raise RuntimeError("Operação inválida")

    def encaminhar(self):
        raise RuntimeError("Operação inválida")

    def finalizar(self):
        raise RuntimeError("Operação inválida")


class RascunhoState(StateDenuncia):
    def salvar(self):
        self.denuncia = StatusDenuncia.SALVO
        self.denuncia.save()


class SalvoState(StateDenuncia):
    def validar(self):
        self.denuncia = StatusDenuncia.VALIDADA
        self.denuncia.save()


class ValidadaState(StateDenuncia):
    def encaminhar(self):
        self.denuncia = StatusDenuncia.ENCAMINHADA
        self.denuncia.save()


class EncaminharState(StateDenuncia):
    def finalizar(self):
        self.denuncia = StatusDenuncia.FINALIZADA
        self.denuncia.save()

