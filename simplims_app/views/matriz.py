"""
Tudo o que é relativo às views de Matriz ficam aqui
"""

from django.urls import reverse_lazy
from django.views.generic import CreateView, DeleteView, ListView, UpdateView

from ..forms import MatrizForm
from ..models import Matriz
from .mixins import DeleteRecordMixin


class MatrizViewMixin:
    """
    Mixin para views de Matriz: define model, form e URL de sucesso.
    """

    model = Matriz
    form_class = MatrizForm
    success_url = reverse_lazy("matriz_listar")


class MatrizListView(MatrizViewMixin, ListView):
    # context_object_name = "matriz"
    template_name = "simplims_app/matriz/lista.html"


class MatrizCreateView(MatrizViewMixin, CreateView):
    template_name = "simplims_app/matriz/formulario.html"


class MatrizUpdateView(MatrizViewMixin, UpdateView):
    template_name = "simplims_app/matriz/formulario.html"


class MatrizDeleteView(MatrizViewMixin, DeleteRecordMixin, DeleteView):
    template_name = "simplims_app/matriz/confirmar_exclusao.html"
