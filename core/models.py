from django.db import models
from django.core.exceptions import ValidationError


class ConfiguracaoApp(models.Model):
    tempo_expiracao_denuncia = models.TimeField()

    def save(self, *args, **kwargs):
        if not self.pk and ConfiguracaoApp.objects.exists():
            raise ValidationError("Já existe uma configuração cadastrada.")
        super().save(*args, **kwargs)

    def __str__(self):
        return "Configurações da Aplicação"
    


class Endereco(models.Model):
    lagradouro = models.CharField(max_length=100, null=True, blank=True)
    numero = models.CharField(max_length=10, null=True, blank=True)
    bairro = models.CharField(max_length=50, null=True, blank=True)
    cidade = models.CharField(max_length=50, null=True, blank=True)
    estado = models.CharField(max_length=2, null=True, blank=True)
    complemento = models.CharField(max_length=50, null=True, blank=True)

    def __str__(self):
        return f'{self.lagradouro}, N.{self.numero}, {self.complemento}, {self.cidade} - {self.estado}'
