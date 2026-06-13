from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse

from auditoria.services.pdf_relatorio import GeradorPDFDenuncia

from denuncia.models import Denuncia


def baixar_pdf(request, denuncia_id):

    denuncia = get_object_or_404(
        Denuncia,
        id=denuncia_id
    )

    pdf = GeradorPDFDenuncia().gerar(
        denuncia
    )

    response = HttpResponse(
        pdf,
        content_type='application/pdf'
    )

    response['Content-Disposition'] = (
        f'attachment; filename="denuncia_{denuncia.id}.pdf"'
    )

    return response
