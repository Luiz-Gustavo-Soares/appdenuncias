from django import forms
from denuncia.models import Denuncia


class DenunciaForm(forms.ModelForm):
    class Meta:
        
        model = Denuncia

        fields = [
            'registrou_anteriormente',
            'situacao_anterior',
            'denunciante_envolvida',
        ]

        widgets = {
            
        }