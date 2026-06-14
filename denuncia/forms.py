from django import forms
from denuncia.models import DenunciaBaseInfo


class DenunciaBaseInfoForm(forms.ModelForm):

    end_logradouro = forms.CharField(
        required=False,
        widget=forms.HiddenInput()
    )

    end_numero = forms.CharField(
        required=False,
        widget=forms.HiddenInput()
    )

    end_bairro = forms.CharField(
        required=False,
        widget=forms.HiddenInput()
    )

    end_cidade = forms.CharField(
        required=False,
        widget=forms.HiddenInput()
    )

    end_estado = forms.CharField(
        required=False,
        widget=forms.HiddenInput()
    )

    end_complemento = forms.CharField(
        required=False,
        widget=forms.HiddenInput()
    )

    class Meta:
        model = DenunciaBaseInfo

        fields = (
            'registrou_anteriormente',
            'situacao_anterior',
            'denunciante_envolvida',
            'perigo_imediato'
        )

        widgets = {
            'registrou_anteriormente': forms.HiddenInput(),
            'situacao_anterior': forms.HiddenInput(),
            'denunciante_envolvida': forms.HiddenInput(),
            'perigo_imediato': forms.HiddenInput(),
        }