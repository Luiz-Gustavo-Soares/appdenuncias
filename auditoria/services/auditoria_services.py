from auditoria.models import AuditoriaAdministrativa

def validar_revisao(denuncia):
    existe = AuditoriaAdministrativa.objects.filter(denuncia=denuncia).exists()
    
    if not existe:
        raise RuntimeError('Não existe uma auditoria para esta denuncia')
    
    return True