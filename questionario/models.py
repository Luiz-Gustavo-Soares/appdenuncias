from django.db import models
from questionario.enums import TipoResposta



class Pergunta(models.Model):
    pergunta = models.TextField()
    tipo = models.CharField(
        choices=TipoResposta.choices,
        max_length=2,
    )

    def qnt_opcoes(self):
        return self.opcoes.count()
    
    def __str__(self):
        return f'Pergunta - {self.id}'


class Opcao(models.Model):
    pergunta = models.ForeignKey(
        Pergunta,
        on_delete=models.CASCADE,
        related_name="opcoes"
    )

    texto = models.CharField(max_length=255)

    pontuacao_risco = models.IntegerField(
        default=0
    )



# pergunta = Pergunta.objects.filter(tipo='TX').first()
# pergunta.qnt_opcoes()
# for op in pergunta.opcoes.all():
#     print(op.texto)



# Opcao.objects.filter().pergunta