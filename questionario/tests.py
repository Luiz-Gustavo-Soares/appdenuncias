from django.test import TestCase

from questionario.models import Questionario
from questionario.enums import SimNao, Frequencia


class QuestionarioTest(TestCase):

    def test_criacao_questionario(self):

        q = Questionario.objects.create(
            agressor_mora_com_vitima=SimNao.SIM,
            agressor_possui_arma=SimNao.SIM,
            houve_ameaca_morte=SimNao.SIM,
            agressao_fisica_recente=SimNao.NAO,
            possui_medida_protetiva=SimNao.NAO,
            descumprimento_medida_protetiva=SimNao.NAO,
            ha_criancas_envolvidas=SimNao.SIM,
            humilhacoes_constantes=Frequencia.FREQUENTEMENTE,
            relato_ocorrido="Teste"
        )

        if(q.agressor_possui_arma == SimNao.SIM):
            print("Possui")
        else:
            print("Não possui")