from django import forms

from questionario.models import Questionario


class QuestionarioForm(forms.ModelForm):

    class Meta:
        model = Questionario
        fields = "__all__"