from django.db import models


class TipoResposta(models.TextChoices):
        TEXTO = "TX", "Texto"
        ESCOLHA_UNICA = "EU", "Escolha Única"
        MULTIPLA_ESCOLHA = "ME", "Múltipla Escolha"