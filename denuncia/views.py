from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse
from denuncia.models import Denuncia
from denuncia.services.denuncia_service import DenunciaService
from django.contrib import messages

def marcar_como_validada(request, denuncia_id):

    denuncia = get_object_or_404(
        Denuncia,
        pk=denuncia_id
    )

    try:
        DenunciaService.validar(denuncia)

        messages.success(
            request,
            "Denúncia marcada como analisada.",
        )
    except RuntimeError as e:
        messages.error(
            request,
            f"Impossivel Marcar como Revisada. {str(e)}",
        )

    return redirect(
        reverse(
            "admin:denuncia_denuncia_change",
            args=[denuncia.pk]
        )
    )
