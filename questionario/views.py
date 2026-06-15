# questionario/views.py

from django.shortcuts import render, redirect

from questionario.forms import QuestionarioForm


def responder_questionario(request):

    if request.method == "POST":

        form = QuestionarioForm(request.POST)

        if form.is_valid():

            form.save()

            return redirect("/")

    else:

        form = QuestionarioForm()

    return render(
        request,
        "questionario/formulario.html",
        {
            "form": form
        }
    )