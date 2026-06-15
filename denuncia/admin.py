from django.contrib import admin
from unfold.admin import ModelAdmin, TabularInline, StackedInline
from django.urls import path
from django.utils.html import format_html
from django.urls import reverse

from denuncia.models import Denuncia, DenunciaBaseInfo, Evidencia
from denuncia.views import marcar_como_validada

from auditoria.views import  baixar_pdf
from auditoria.models import AuditoriaAdministrativa

from questionario.models import Questionario



class EvidenciaInline(TabularInline):
    model = Evidencia
    extra = 0
    readonly_fields = ('download',)

    

class AuditoriaAdmInline(TabularInline):
    model = AuditoriaAdministrativa
    extra = 0
    can_delete = False

class DenunciaBaseInfoInline(StackedInline):
    model = DenunciaBaseInfo
    extra = 0
    can_delete = False
    show_change_link = True

class QuestionarioInline(StackedInline):
    model = Questionario
    extra = 0
    can_delete = False
    show_change_link = True


styling_button = "padding: 10px;  text-align: center; margin: 2px 5px 2px 5px; background-color: #b6b6b63b; border-radius:5px;"

@admin.register(Denuncia)
class DenunciaAdmin(ModelAdmin):
    list_display = ('data_criacao', 'risco_automatico', 'auditoria__nivel_risco_corrigido', 'status')
    
    list_filter = ('data_criacao', 'risco_automatico', 'auditoria__nivel_risco_corrigido')
    
    readonly_fields = ("botao_pdf", "revisao")

    inlines = [
        AuditoriaAdmInline,
        DenunciaBaseInfoInline, 
        QuestionarioInline,
        EvidenciaInline,
        ]



    def has_delete_permission(self, request, obj=None):
        return False


    def botao_pdf(self, obj):

        if not obj.pk:
            return "-"

        url = reverse(
            "admin:denuncia_pdf",
            args=[obj.pk]
        )

        return format_html(
            '<a style="{} display: block;" class="button" href="{}">Gerar PDF</a>',
            styling_button, url
        )

    def revisao(self, obj):

        if not obj.pk:
            return "-"

        url_validar = reverse(
            "admin:validar",
            args=[obj.pk]
        )

        

        return format_html(
            '''
            <div style="display: flex; align-items: center; justify-content: center;">
                <a style="{}" class="button" href="{}">Marcar como Validada</a>
                <a style="{}" class="button" href="#">Encaminhar</a>
                <a style="{}" class="button" href="#">Finalizar</a>
            </div>
            ''',
            styling_button, url_validar,
            styling_button,
            styling_button,
        )


    def get_urls(self):

        urls = super().get_urls()

        custom_urls = [
            path(
                "<int:denuncia_id>/pdf/",
                self.admin_site.admin_view(
                    baixar_pdf
                ),
                name="denuncia_pdf",
            ),
            path(
                "<int:denuncia_id>/validar/",
                self.admin_site.admin_view(
                    marcar_como_validada
                ),
                name="validar",
            ),
        ]

        return custom_urls + urls
