from django.urls import path

from questionario.views import responder_questionario

urlpatterns = [
    path("", responder_questionario, name="questionario"),
]