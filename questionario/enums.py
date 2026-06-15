from django.db import models

class Relacao(models.TextChoices):
    CONJUGUE = "CO", "Cônjuge"
    EX_CONJUGUE = "EC", "Ex-cônjuge"
    NAMORADO = "NA", "Namorado(a)"
    EX_NAMORADO = "EN", "Ex-namorado(a)"
    FAMILIAR = "FA", "Familiar"
    CONHECIDO = "CN", "Conhecido(a)"
    DESCONHECIDO = "DE", "Desconhecido(a)"

class OndeOcorreu(models.TextChoices):
    RESIDENCIA_VITIMA = "RV", "Residência da vítima"
    RESIDENCIA_AUTOR = "RA", "Residência do autor"
    RESIDENCIA_COMUM = "RC", "Residência comum"
    VIA_PUBLICA = "VP", "Via pública"
    LOCAL_TRABALHO = "LT", "Local de trabalho"
    OUTRO = "OU", "Outro"

class SimNaoNaoSei(models.TextChoices):
    SIM = "SI", "Sim"
    NAO = "NA", "Não"
    NAO_SEI = "NS", "Não sei"

class ArmaInstrumento(models.TextChoices):
    NENHUM = "NE", "Nenhum"
    ARMA_DE_FOGO = "AF", "Arma de fogo"
    ARMA_BRANCA = "AB", "Arma branca"
    OBJETO_CONTUNDENTE = "OC", "Objeto contundente"
    OUTRO = "OU", "Outro"

class TipoVeiculo(models.TextChoices):
    CARRO = "CA", "Carro"
    MOTO = "MO", "Moto"
    CAMINHAO = "CM", "Caminhão"
    ONIBUS = "ON", "Ônibus"
    OUTRO = "OU", "Outro"

#
class SimNao(models.TextChoices):
    SIM = "SI", "Sim"
    NAO = "NA", "Não"


class Frequencia(models.TextChoices):
    NUNCA = "NU", "Nunca"
    RARAMENTE = "RA", "Raramente"
    FREQUENTEMENTE = "FR", "Frequentemente"


class NivelRisco(models.TextChoices):
    BAIXO = "BA", "Baixo"
    MEDIO = "ME", "Médio"
    ALTO = "AL", "Alto"
    CRITICO = "CR", "Crítico"


class TipoViolencia(models.TextChoices):
    FISICA = "FI", "Física"
    PSICOLOGICA = "PS", "Psicológica"
    SEXUAL = "SE", "Sexual"
    MORAL = "MO", "Moral"
    PATRIMONIAL = "PA", "Patrimonial"