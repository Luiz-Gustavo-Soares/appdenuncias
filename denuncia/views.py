from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import FileResponse
from django.core.exceptions import PermissionDenied

from denuncia.models import Denuncia, Evidencia, DenunciaBaseInfo
from denuncia.services.denuncia_service import DenunciaService
from core.models import Endereco



@login_required
def visualizar_evidencia(request, evidencia_id):

    evidencia = get_object_or_404(
        Evidencia,
        pk=evidencia_id
    )

    if not request.user.is_staff:
        raise PermissionDenied()
    
    return FileResponse(
        evidencia.arquivo.open("rb"),
        as_attachment=False
    )



def marcar_como_validada(request, denuncia_id):

    denuncia = get_object_or_404(
        Denuncia,
        pk=denuncia_id
    )

    try:
        DenunciaService.validar(denuncia)

        messages.success(
            request,
            "Denúncia marcada como validada.",
        )
    except RuntimeError as e:
        messages.error(
            request,
            f"Impossivel Marcar como validada. {str(e)}",
        )

    return redirect(
        reverse(
            "admin:denuncia_denuncia_change",
            args=[denuncia.pk]
        )
    )


def triagem(request):
    if request.method == 'POST':
        request.session['triagem'] = request.POST.dict()
        
        registrou_anteriormente = (
            request.POST.get('ocorrencia_anterior') == 'sim'
        )

        situacao_anterior = request.POST.get('situacao_anterior')
        
        perigo_imediato = (
            request.POST.get('perigo_imediato') == 'sim'
        )

        denunciante_envolvida = (
            request.POST.get('vitima') == 'sim'
        )

        endereco = Endereco.objects.create(
            lagradouro=request.POST.get('end_logradouro'),
            numero=request.POST.get('end_numero'),
            bairro=request.POST.get('end_bairro'),
            cidade=request.POST.get('end_cidade'),
            estado=request.POST.get('end_estado'),
            complemento=request.POST.get('end_complemento'),
        )

        denuncia = Denuncia.objects.create()
        denuncia_info = DenunciaBaseInfo.objects.create(
            denuncia=denuncia, 
            perigo_imediato=perigo_imediato, 
            registrou_anteriormente=registrou_anteriormente, 
            situacao_anterior=situacao_anterior, 
            denunciante_envolvida=denunciante_envolvida, 
            endereco=endereco
        )

        return redirect('denuncia:registro')



    return redirect('index')

def registro(request):
    return render(request, 'denuncia/registro.html')
