from django.contrib import admin
from unfold.admin import ModelAdmin, TabularInline, StackedInline
from django.urls import path
from django.utils.html import format_html
from django.urls import reverse

from denuncia.models import Denuncia, DenunciaBaseInfo, Evidencia
from denuncia.views import marcar_como_validada

from auditoria.views import  baixar_pdf
from auditoria.models import AuditoriaAdministrativa



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


@admin.action(description="Marcar denuncia como revisada")
def tornar_gerente(modeladmin, request, queryset):
    queryset.update(cargo='Gerente')


@admin.register(Denuncia)
class DenunciaAdmin(ModelAdmin):
    list_display = ('data_criacao', 'risco_automatico', 'auditoria__nivel_risco_corrigido', 'status')
    
    list_filter = ('data_criacao', 'risco_automatico', 'auditoria__nivel_risco_corrigido')
    
    readonly_fields = ("botao_pdf", "revisao")

    inlines = [
        AuditoriaAdmInline,
        DenunciaBaseInfoInline, 
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
            '<a style="padding: 10px; display: block" class="button" href="{}">Gerar PDF</a>',
            url
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
            <div>
                <a style="padding: 10px; display: block text-aling: center;" class="button" href="{}">Marcar como Validada</a>
                <a style="padding: 10px; display: block text-aling: center;" class="button" href="#">Encaminhar</a>
                <a style="padding: 10px; display: block text-aling: center;" class="button" href="#">Finalizar</a>
            </div>
            ''',
            url_validar
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
