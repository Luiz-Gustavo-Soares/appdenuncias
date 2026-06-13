from django import forms
from core.models import Endereco

class EnderecoForm(forms.ModelForm):
    class Meta:
        model = Endereco