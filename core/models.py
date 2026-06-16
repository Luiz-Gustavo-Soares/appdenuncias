from django.db import models
from django.core.exceptions import ValidationError




class Endereco(models.Model):
    lagradouro = models.CharField(max_length=150, null=True, blank=True)
    numero = models.CharField(max_length=10, null=True, blank=True)
    bairro = models.CharField(max_length=50, null=True, blank=True)
    cidade = models.CharField(max_length=50, null=True, blank=True)
    estado = models.CharField(max_length=2, null=True, blank=True)
    complemento = models.CharField(max_length=50, null=True, blank=True)

    def __str__(self):
        return f'{self.lagradouro}, N.{self.numero}, {self.complemento}, {self.cidade} - {self.estado}'
