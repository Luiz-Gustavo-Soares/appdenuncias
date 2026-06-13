from django.contrib import admin
from denuncia.models import Denuncia


class DenunciaAdmin(admin.ModelAdmin):
    list_display = ('data_criacao', 'nivel_risco', 'status')
    
    list_filter = ('data_criacao', 'nivel_risco')
    

    def has_delete_permission(self, request, obj=None):
        return False


admin.site.register(Denuncia, DenunciaAdmin)