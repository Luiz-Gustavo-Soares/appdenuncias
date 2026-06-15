from django import forms

from questionario.models import Questionario

# FORM TESTE SO PARA VER SE FUNCIONOU PODE APAGAR CALABRESO
class QuestionarioForm(forms.ModelForm):

    class Meta:
        model = Questionario
        fields = "__all__"

        widgets = {
            "data_fato": forms.DateInput(attrs={"type": "date"}),
            "data_nascimento_vitima": forms.DateInput(attrs={"type": "date"}),
            "hora_aproximada_fato": forms.TimeInput(attrs={"type": "time"}),
        }