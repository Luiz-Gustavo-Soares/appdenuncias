from django.http import HttpResponse
from django.shortcuts import render

def my_view(request):
    # Returns raw HTML directly to the browser
    
    nome = request.GET.get('nome', 'O Sem Nome')

    
    context = {
        'nome': nome,
        'qnt': range(5)
    }

    return render(request, 'index.html', context)


def my_view_parametros(request, nome):
    return HttpResponse(f"<h1>Ola, {nome}</h1>", content_type="text/html")
