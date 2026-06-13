from django.db import models


class StatusDenuncia(models.TextChoices):
    RASCUNHO = "RA", "Rascunho"
    SALVO = "SV", "Salvo"
    VALIDADA = "VA", "Validada"
    ENCAMINHADA = "EC", "Encaminhada"
    FINALIZADA = "FI", "Finalizada"


class NivelDeRisco(models.TextChoices):
    CRITICO = "CR", "Critico"
    ALTO = "AL", "Alto"
    MEDIO = "ME", "Medio"
    BAIXO = "BA", "Baixo"
