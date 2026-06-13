from django.shortcuts import render, redirect

def triagem(request):
    if request.method == 'POST':
        # Salva os dados da triagem na sessão
        request.session['triagem'] = request.POST.dict()
        return redirect('denuncia:registro')  # ← redireciona para o registro
    # GET direto nessa URL volta para a landing
    return redirect('index')

def registro(request):
    return render(request, 'denuncia/registro.html')