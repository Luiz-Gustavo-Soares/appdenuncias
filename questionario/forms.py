from django import forms

from questionario.models import Questionario


# forms.py

from django import forms

from .models import Questionario


class QuestionarioForm(forms.ModelForm):

    class Meta:
        model = Questionario
        fields = [
            "relacao_com_vitima",
            "onde_ocorreu",
            "ha_risco_integridade_fisica",
            "ha_criancas_adolescentes_envolvidos",
            "data_fato",
            "hora_aproximada_fato",
            "logradouro_fato",
            "numero_fato",
            "bairro_fato",
            "cidade_fato",
            "estado_fato",
            "nome_completo_vitima",
            "data_nascimento_vitima",
            "cpf_vitima",
            "telefone_vitima",
            "email_vitima",
            "endereco_residencial_vitima",
            "nome_completo_autor",
            "idade_aproximada_autor",
            "cpf_autor",
            "caracteristicas_fisicas_autor",
            "endereco_conhecido_autor",
            "tipo_veiculo_autor",
            "placa_veiculo_autor",
            "cor_veiculo_autor",
            "modelo_marca_veiculo_autor",
            "arma_ou_instrumento_utilizado",
            "objetos_subtraidos",
            "descricao_ocorrencia",
            "informacoes_testemunhas",
            "violencia_recorrente",
            "medida_protetiva_em_vigor",
            "vitima_deseja_representar_criminalmente",
        ]

        widgets = {

        # =====================
        # ETAPA 1
        # =====================

        "relacao_com_vitima": forms.Select(
            attrs={
                "id": "relacao_autora",
                "class": "campo__select",
            }
        ),

        "onde_ocorreu": forms.Select(
            attrs={
                "id": "local_fato",
                "class": "campo__select",
            }
        ),

        "ha_risco_integridade_fisica": forms.RadioSelect(
            attrs={
                "id": "risco_iminente",
                "class": "campo__radio"
            }
        ),

        "ha_criancas_adolescentes_envolvidos": forms.RadioSelect(
            attrs={
                "id": "criancas_envolvidas",
                "class": "campo__radio"
            }
        ),

        # =====================
        # ETAPA 2
        # =====================

        "data_fato": forms.DateInput(
            attrs={
                "id": "data_fato",
                "class": "campo__input",
                "type": "date",
            }
        ),

        "hora_aproximada_fato": forms.TimeInput(
            attrs={
                "id": "hora_fato",
                "class": "campo__input",
                "type": "time",
            }
        ),

        "logradouro_fato": forms.TextInput(
            attrs={
                "id": "logradouro_fato",
                "class": "campo__input",
                "placeholder": "Rua, Avenida, Travessa...",
            }
        ),

        "numero_fato": forms.TextInput(
            attrs={
                "id": "numero_fato",
                "class": "campo__input",
                "placeholder": "Nº",
            }
        ),

        "bairro_fato": forms.TextInput(
            attrs={
                "id": "bairro_fato",
                "class": "campo__input",
            }
        ),

        "cidade_fato": forms.TextInput(
            attrs={
                "id": "cidade_fato",
                "class": "campo__input",
            }
        ),

        "estado_fato": forms.TextInput(
            attrs={
                "id": "estado_fato",
                "class": "campo__input",
                "maxlength": "2",
                "placeholder": "UF",
            }
        ),

        # =====================
        # ETAPA 3
        # =====================

        "nome_completo_vitima": forms.TextInput(
            attrs={
                "id": "vitima_nome",
                "class": "campo__input",
            }
        ),

        "data_nascimento_vitima": forms.DateInput(
            attrs={
                "id": "vitima_nascimento",
                "class": "campo__input",
                "type": "date",
            }
        ),

        "cpf_vitima": forms.TextInput(
            attrs={
                "id": "vitima_cpf",
                "class": "campo__input",
                "maxlength": "14",
                "placeholder": "000.000.000-00",
            }
        ),

        "telefone_vitima": forms.TextInput(
            attrs={
                "id": "vitima_telefone",
                "class": "campo__input",
                "placeholder": "(00) 00000-0000",
            }
        ),

        "email_vitima": forms.EmailInput(
            attrs={
                "id": "vitima_email",
                "class": "campo__input",
            }
        ),

        "endereco_residencial_vitima": forms.TextInput(
            attrs={
                "id": "vitima_endereco",
                "class": "campo__input",
                "placeholder": "Logradouro, número, bairro, cidade - UF",
            }
        ),

        # =====================
        # ETAPA 4
        # =====================

        "nome_completo_autor": forms.TextInput(
            attrs={
                "id": "autor_nome",
                "class": "campo__input",
            }
        ),

        "idade_aproximada_autor": forms.NumberInput(
            attrs={
                "id": "autor_idade",
                "class": "campo__input",
            }
        ),

        "cpf_autor": forms.TextInput(
            attrs={
                "id": "autor_cpf",
                "class": "campo__input",
                "maxlength": "14",
                "placeholder": "000.000.000-00",
            }
        ),

        "caracteristicas_fisicas_autor": forms.Textarea(
            attrs={
                "id": "autor_caracteristicas",
                "class": "campo__textarea",
                "rows": 3,
                "placeholder": "Altura, cor de cabelo, porte, tatuagens, etc.",
            }
        ),

        "endereco_conhecido_autor": forms.TextInput(
            attrs={
                "id": "autor_endereco",
                "class": "campo__input",
                "placeholder": "Logradouro, número, bairro, cidade - UF",
            }
        ),

        # =====================
        # ETAPA 5
        # =====================

        "tipo_veiculo_autor": forms.Select(
            attrs={
                "id": "veiculo_tipo",
                "class": "campo__select",
            }
        ),

        "placa_veiculo_autor": forms.TextInput(
            attrs={
                "id": "veiculo_placa",
                "class": "campo__input",
                "maxlength": "8",
                "placeholder": "AAA-0000",
            }
        ),

        "cor_veiculo_autor": forms.TextInput(
            attrs={
                "id": "veiculo_cor",
                "class": "campo__input",
            }
        ),

        "modelo_marca_veiculo_autor": forms.TextInput(
            attrs={
                "id": "veiculo_modelo",
                "class": "campo__input",
            }
        ),

        # =====================
        # ETAPA 6
        # =====================

        "arma_ou_instrumento_utilizado": forms.Select(
            attrs={
                "id": "objetos_arma",
                "class": "campo__select",
            }
        ),

        "objetos_subtraidos": forms.Textarea(
            attrs={
                "id": "objetos_subtraidos",
                "class": "campo__textarea",
                "rows": 3,
                "placeholder": "Descreva os objetos, se houver...",
            }
        ),

        # =====================
        # ETAPA 7
        # =====================

        "descricao_ocorrencia": forms.Textarea(
            attrs={
                "id": "descricao_fato",
                "class": "campo__textarea campo__textarea--grande",
                "rows": 10,
                "placeholder": (
                    "Descreva o que ocorreu, quando, como e qualquer detalhe relevante..."
                ),
            }
        ),

        "informacoes_testemunhas": forms.Textarea(
            attrs={
                "id": "testemunhas",
                "class": "campo__textarea",
                "rows": 3,
                "placeholder": (
                    "Nome e telefone das testemunhas, se houver..."
                ),
            }
        ),

        # =====================
        # ETAPA 8
        # =====================

        "violencia_recorrente": forms.RadioSelect(
            attrs={
                "class": "campo__radio"
            }
        ),

        "medida_protetiva_em_vigor": forms.RadioSelect(
            attrs={
                "class": "campo__radio"
            }
        ),

        "vitima_deseja_representar_criminalmente": forms.RadioSelect(
            attrs={
                "class": "campo__radio"
            }
        ),
    }
