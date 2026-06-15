from django.db import models

from questionario.enums import (
    SimNao,
    SimNaoNaoSei,
    TipoVeiculo,
    ArmaInstrumento,
    Relacao,
    OndeOcorreu
)


class Questionario(models.Model):

    # Questionário Inicial
    relacao_com_vitima = models.CharField(
        max_length=2,
        choices=Relacao.choices
    )

    onde_ocorreu = models.CharField(
        max_length=2,
        choices=OndeOcorreu.choices
    )

    ha_risco_integridade_fisica = models.CharField(
        max_length=2,
        choices=SimNaoNaoSei.choices,
        blank=True
    )

    ha_criancas_adolescentes_envolvidos = models.CharField(
        max_length=2,
        choices=SimNao.choices,
        blank=True
    )

    # Dados básicos
    data_fato = models.DateField()

    hora_aproximada_fato = models.TimeField(
        blank=True,
        null=True
    )

    logradouro_fato = models.CharField(
        max_length=255
    )

    numero_fato = models.CharField(
        max_length=20,
        blank=True
    )

    bairro_fato = models.CharField(
        max_length=100,
        blank=True
    )

    cidade_fato = models.CharField(
        max_length=100,
        blank=True
    )

    estado_fato = models.CharField(
        max_length=2,
        blank=True
    )    

    # Dados da vítima
    nome_completo_vitima = models.CharField(
        max_length=255
    )

    data_nascimento_vitima = models.DateField(
        blank=True,
        null=True
    )

    cpf_vitima = models.CharField(
        max_length=14,
        blank=True
    )

    telefone_vitima = models.CharField(
        max_length=20,
        blank=True
    )

    email_vitima = models.EmailField(
        blank=True
    )

    endereco_residencial_vitima = models.CharField(
        max_length=255,
        blank=True
    )

    # Dados do autor
    nome_completo_autor = models.CharField(
        max_length=255,
        blank=True
    )

    idade_aproximada_autor = models.PositiveSmallIntegerField(
        blank=True,
        null=True
    )

    cpf_autor = models.CharField(
        max_length=14,
        blank=True
    )

    caracteristicas_fisicas_autor = models.TextField(
        blank=True
    )

    endereco_conhecido_autor = models.CharField(
        max_length=255,
        blank=True
    )

    # Veículos envolvidos
    tipo_veiculo_autor = models.CharField(
        max_length=2,
        choices=TipoVeiculo.choices,
        blank=True
    )

    placa_veiculo_autor = models.CharField(
        max_length=8,
        blank=True
    )

    cor_veiculo_autor = models.CharField(
        max_length=50,
        blank=True
    )

    modelo_marca_veiculo_autor = models.CharField(
        max_length=100,
        blank=True
    )

    # Objetos envolvidos
    arma_ou_instrumento_utilizado = models.CharField(
        max_length=2,
        choices=ArmaInstrumento.choices,
        blank=True
    )

    objetos_subtraidos = models.TextField(
        blank=True
    )

    # Descrição do fato
    descricao_ocorrencia = models.TextField()

    informacoes_testemunhas = models.TextField(
        blank=True
    )

    # Questões complementares
    violencia_recorrente = models.CharField(
        max_length=2,
        choices=SimNaoNaoSei.choices,
        blank=True
    )

    medida_protetiva_em_vigor = models.CharField(
        max_length=2,
        choices=SimNaoNaoSei.choices,
        blank=True
    )

    vitima_deseja_representar_criminalmente = models.CharField(
        max_length=2,
        choices=SimNaoNaoSei.choices,
        blank=True
    )

    def __str__(self):
        return f"Questionário {self.id}"