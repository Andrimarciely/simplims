"""
Tudo o que é relativo às views de ServicoContratado ficam aqui
"""

from django.urls import reverse_lazy
from django.views.generic import CreateView, DeleteView, ListView, UpdateView

from ..forms import ServicoContratadoForm
from ..forms import ServicoForm
from ..models import ServicoContratado
from ..models import Servico
from .mixins import DeleteRecordMixin


class ServicoContratadoViewMixin:
    """
    Mixin para views de ServicoContratado: define model, form e URL de sucesso.
    """

    model = ServicoContratado
    form_class = ServicoForm
    success_url = reverse_lazy("servico_contratado_listar")


class ServicoContratadoListView(ServicoContratadoViewMixin, ListView):
    # context_object_name = "servico_contratado"
    template_name = "simplims_app/servico_contratado/lista.html"


class ServicoContratadoCreateView(ServicoContratadoViewMixin, CreateView):
    template_name = "simplims_app/servico_contratado/formulario.html"


class ServicoContratadoUpdateView(ServicoContratadoViewMixin, UpdateView):
    template_name = "simplims_app/servico_contratado/formulario.html"


class ServicoContratadoDeleteView(ServicoContratadoViewMixin, DeleteRecordMixin, DeleteView):
    template_name = "simplims_app/servico_contratado/confirmar_exclusao.html"
