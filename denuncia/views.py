from django.shortcuts import render, redirect
from django.views.decorators.cache import never_cache

@never_cache
def triagem(request):
    if request.method == 'POST':
        request.session['triagem'] = request.POST.dict()
        return redirect('denuncia:registro')
    return redirect('index')

@never_cache
def registro(request):
    return render(request, 'denuncia/registro.html')