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
    Define o comportamento comum das views de ServicoContratado.
    """
    model = ServicoContratado
    form_class = ServicoContratadoForm
    success_url = reverse_lazy("servico_contratado_listar")
    ordering = ['-id']

    def get_ordem_servico_id(self):
        """
        Método auxiliar opcional para capturar o ID da ordem de serviço via GET.
        Pode ser usado em CreateView ou em outros contextos específicos.
        """
        return self.request.GET.get("ordem_servico")


class ServicoContratadoListView(ServicoContratadoViewMixin, ListView):
    # context_object_name = "servico_contratado"
    template_name = "simplims_app/servico_contratado/lista.html"


class ServicoContratadoCreateView(ServicoContratadoViewMixin, CreateView):
    template_name = "simplims_app/servico_contratado/formulario.html"

    def get_initial(self):
        initial = super().get_initial()
        ordem_servico_id = self.request.GET.get("ordem_servico")
        if ordem_servico_id:
            initial["ordem_servico"] = ordem_servico_id
        return initial

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        ordem_servico_id = self.request.GET.get("ordem_servico")
        context["ordem_servico_id"] = ordem_servico_id
        return context


class ServicoContratadoUpdateView(ServicoContratadoViewMixin, UpdateView):
    template_name = "simplims_app/servico_contratado/formulario.html"


class ServicoContratadoDeleteView(ServicoContratadoViewMixin, DeleteRecordMixin, DeleteView):
    template_name = "simplims_app/servico_contratado/confirmar_exclusao.html"
