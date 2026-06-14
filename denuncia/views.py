from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import FileResponse
from django.core.exceptions import PermissionDenied

from denuncia.models import Denuncia, Evidencia
from denuncia.services.denuncia_service import DenunciaService


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
        # Salva os dados da triagem na sessão
        request.session['triagem'] = request.POST.dict()
        return redirect('denuncia:registro')  # ← redireciona para o registro
    # GET direto nessa URL volta para a landing
    return redirect('index')

def registro(request):
    return render(request, 'denuncia/registro.html')
