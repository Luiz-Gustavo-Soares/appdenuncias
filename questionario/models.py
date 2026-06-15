from django.db import models
from denuncia.models import Denuncia

from questionario.enums import (
    SimNao,
    SimNaoNaoSei,
    TipoVeiculo,
    ArmaInstrumento,
    Relacao,
    OndeOcorreu
)


class Questionario(models.Model):
    denuncia = models.OneToOneField(
        Denuncia,
        on_delete=models.PROTECT,
        related_name='questionario'
    )

    # Questionário Inicial
    relacao_com_vitima = models.CharField(
        max_length=2,
        choices=Relacao.choices,
        null=True
    )

    onde_ocorreu = models.CharField(
        max_length=2,
        choices=OndeOcorreu.choices,
        null=True
    )

    ha_risco_integridade_fisica = models.CharField(
        max_length=2,
        choices=SimNaoNaoSei.choices,
        default=SimNaoNaoSei.NAO_SEI,
        null=True
    )

    ha_criancas_adolescentes_envolvidos = models.CharField(
        max_length=2,
        choices=SimNaoNaoSei.choices,
        default=SimNaoNaoSei.NAO_SEI,
        null=True
    )

    # Dados básicos
    data_fato = models.DateField(blank=True, null=True)

    hora_aproximada_fato = models.TimeField(
        blank=True,
        null=True
    )

    logradouro_fato = models.CharField(
        max_length=255
    )

    numero_fato = models.CharField(
        max_length=20,
        blank=True, null=True
    )

    bairro_fato = models.CharField(
        max_length=100,
        blank=True, null=True
    )

    cidade_fato = models.CharField(
        max_length=100,
        blank=True, null=True
    )

    estado_fato = models.CharField(
        max_length=2,
        blank=True, null=True
    )    

    # Dados da vítima
    nome_completo_vitima = models.CharField(
        max_length=255,
        blank=True,
        null=True
    )

    data_nascimento_vitima = models.DateField(
        blank=True,
        null=True
    )

    cpf_vitima = models.CharField(
        max_length=14,
        blank=True, null=True
    )

    telefone_vitima = models.CharField(
        max_length=20,
        blank=True, null=True
    )

    email_vitima = models.EmailField(
        blank=True, null=True
    )

    endereco_residencial_vitima = models.CharField(
        max_length=255,
        blank=True, null=True
    )

    # Dados do autor
    nome_completo_autor = models.CharField(
        max_length=255,
        blank=True, null=True
    )

    idade_aproximada_autor = models.PositiveSmallIntegerField(
        blank=True,
        null=True
    )

    cpf_autor = models.CharField(
        max_length=14,
        blank=True, null=True
    )

    caracteristicas_fisicas_autor = models.TextField(
        blank=True, null=True
    )

    endereco_conhecido_autor = models.CharField(
        max_length=255,
        blank=True, null=True
    )

    # Veículos envolvidos
    tipo_veiculo_autor = models.CharField(
        max_length=2,
        choices=TipoVeiculo.choices,
        blank=True, null=True
    )

    placa_veiculo_autor = models.CharField(
        max_length=8,
        blank=True, null=True
    )

    cor_veiculo_autor = models.CharField(
        max_length=50,
        blank=True, null=True
    )

    modelo_marca_veiculo_autor = models.CharField(
        max_length=100,
        blank=True, null=True
    )

    # Objetos envolvidos
    arma_ou_instrumento_utilizado = models.CharField(
        max_length=2,
        choices=ArmaInstrumento.choices,
        blank=True, null=True
    )

    objetos_subtraidos = models.TextField(
        blank=True, null=True
    )

    # Descrição do fato
    descricao_ocorrencia = models.TextField(blank=True, null=True)

    informacoes_testemunhas = models.TextField(
        blank=True, null=True
    )

    # Questões complementares
    violencia_recorrente = models.CharField(
        max_length=2,
        choices=SimNaoNaoSei.choices,
        blank=True, null=True
    )

    medida_protetiva_em_vigor = models.CharField(
        max_length=2,
        choices=SimNaoNaoSei.choices,
        blank=True, null=True
    )

    vitima_deseja_representar_criminalmente = models.CharField(
        max_length=2,
        choices=SimNaoNaoSei.choices,
        blank=True, null=True
    )

    def __str__(self):
        return f"Questionário {self.id}"