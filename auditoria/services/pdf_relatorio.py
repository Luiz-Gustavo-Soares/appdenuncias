from io import BytesIO
from django.template.loader import render_to_string
from weasyprint import HTML


class GeradorPDFDenuncia:

    def gerar(self, denuncia):

        html = render_to_string(
            "pdf/denuncia.html",
            {
                "denuncia": denuncia,
                "evidencias": denuncia.evidencias.all()
            }
        )

        pdf_file = BytesIO()

        HTML(
            string=html
        ).write_pdf(
            pdf_file
        )

        return pdf_file.getvalue()
