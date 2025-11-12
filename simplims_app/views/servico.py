"""
Tudo o que é relativo às views de Servico ficam aqui
"""

from django.urls import reverse_lazy
from django.views.generic import CreateView, DeleteView, ListView, UpdateView

from ..forms import ServicoForm
from ..models import Servico
from .mixins import DeleteRecordMixin


class ServicoViewMixin:
    """
    Mixin para views de Servico: define model, form e URL de sucesso.
    """

    model = Servico
    form_class = ServicoForm
    success_url = reverse_lazy("servico_listar")


class ServicoListView(ServicoViewMixin, ListView):
    # context_object_name = "servico"
    template_name = "simplims_app/servico/lista.html"


class ServicoCreateView(ServicoViewMixin, CreateView):
    template_name = "simplims_app/servico/formulario.html"


class ServicoUpdateView(ServicoViewMixin, UpdateView):
    template_name = "simplims_app/servico/formulario.html"


class ServicoDeleteView(ServicoViewMixin, DeleteRecordMixin, DeleteView):
    template_name = "simplims_app/servico/confirmar_exclusao.html"
