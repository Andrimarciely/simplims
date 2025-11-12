"""
Tudo o que é relativo às views de Legislacao ficam aqui
"""

from django.urls import reverse_lazy
from django.views.generic import CreateView, DeleteView, ListView, UpdateView

from ..forms import LegislacaoForm
from ..models import Legislacao
from .mixins import DeleteRecordMixin


class LegislacaoViewMixin:
    """
    Mixin para views de Legislacao: define model, form e URL de sucesso.
    """

    model = Legislacao
    form_class = LegislacaoForm
    success_url = reverse_lazy("legislacao_listar")


class LegislacaoListView(LegislacaoViewMixin, ListView):
    # context_object_name = "legislacao"
    template_name = "simplims_app/legislacao/lista.html"


class LegislacaoCreateView(LegislacaoViewMixin, CreateView):
    template_name = "simplims_app/legislacao/formulario.html"


class LegislacaoUpdateView(LegislacaoViewMixin, UpdateView):
    template_name = "simplims_app/legislacao/formulario.html"


class LegislacaoDeleteView(LegislacaoViewMixin, DeleteRecordMixin, DeleteView):
    template_name = "simplims_app/legislacao/confirmar_exclusao.html"
