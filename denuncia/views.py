from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import FileResponse
from django.core.exceptions import PermissionDenied
from django.views.decorators.cache import never_cache

from denuncia.models import Denuncia, Evidencia, DenunciaBaseInfo
from denuncia.services.denuncia_service import DenunciaService
from denuncia.enums import StatusDenuncia

from questionario.models import Questionario
from questionario.forms import QuestionarioForm

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


@login_required
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


@login_required
def encaminhar(request, denuncia_id):
    denuncia = get_object_or_404(
        Denuncia,
        pk=denuncia_id
    )

    try:
        DenunciaService.encaminhar(denuncia)

        messages.success(
            request,
            "Denúncia Enviada.",
        )

    except RuntimeError as e:
        messages.error(
            request,
            f"Impossivel enviar. {str(e)}",
        )

    return redirect(
        reverse(
            "admin:denuncia_denuncia_change",
            args=[denuncia.pk]
        )
    )


@login_required
def finalizar(request, denuncia_id):
    denuncia = get_object_or_404(
        Denuncia,
        pk=denuncia_id
    )

    try:
        DenunciaService.finalizar(denuncia, request.user)

        messages.success(
            request,
            "Denúncia Finalizada.",
        )
        
    except RuntimeError as e:
        messages.error(
            request,
            f"Impossivel finalizar. {str(e)}",
        )

    return redirect(
        reverse(
            "admin:denuncia_denuncia_change",
            args=[denuncia.pk]
        )
    )


@never_cache
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

        return redirect('denuncia:registro', denuncia.codigo_denuncia)



    return redirect('index')

@never_cache
def registro(request, codigo_denuncia):
    denuncia = get_object_or_404(
        Denuncia,
        codigo_denuncia=codigo_denuncia
    )

    if not denuncia.status == StatusDenuncia.RASCUNHO:
        return redirect('index')



    if request.method == "POST":
        form = QuestionarioForm(request.POST)
        if form.is_valid:
            questionario = form.save(commit=False)
            questionario.denuncia = denuncia
            questionario.save()

            for arquivo in request.FILES.getlist("anexos"):

                Evidencia.objects.create(
                    denuncia=denuncia,
                    arquivo=arquivo
                )
            
            denuncia.state.salvar()

    form = QuestionarioForm()
    
    context = {
        'denuncia': denuncia, 
        'form': form
        }
    
    return render(request, 'denuncia/registro.html', context)
