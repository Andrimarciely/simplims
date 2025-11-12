"""
Tudo o que é relativo às views de Parametro ficam aqui
"""

from django.urls import reverse_lazy
from django.views.generic import CreateView, DeleteView, ListView, UpdateView
from django.db.models import Q
from ..forms import ParametroForm
from ..models import Parametro
from .mixins import DeleteRecordMixin


class ParametroViewMixin:
    """
    Mixin para views de Parametro: define model, form e URL de sucesso.
    """

    model = Parametro
    form_class = ParametroForm
    success_url = reverse_lazy("parametro_listar")


class ParametroListView(ParametroViewMixin, ListView):
    # context_object_name = "parametro"
    model = Parametro
    template_name = "simplims_app/parametro/lista.html"

    def get_queryset(self):
        qs = super().get_queryset()

        # filtro de busca
        q = self.request.GET.get("q", "").strip()
        if q:
            qs = qs.filter(
                Q(descricao__icontains=q)
                | Q(unidade_medida__icontains=q)
                | Q(categoria_parametro__descricao__icontains=q)
                | Q(tipo_parametro__descricao__icontains=q)
            )

        # ordenação dinâmica
        ordering = self.request.GET.get("ordering", "id")
        allowed_orderings = [
            "id",
            "descricao",
            "unidade_medida",
            "categoria_parametro",
            "tipo_parametro",
        ]
        if ordering.lstrip("-") in allowed_orderings:
            qs = qs.order_by(ordering)

        return qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["q"] = self.request.GET.get("q", "")
        return context


class ParametroCreateView(ParametroViewMixin, CreateView):
    template_name = "simplims_app/parametro/formulario.html"


class ParametroUpdateView(ParametroViewMixin, UpdateView):
    template_name = "simplims_app/parametro/formulario.html"


class ParametroDeleteView(ParametroViewMixin, DeleteRecordMixin, DeleteView):
    template_name = "simplims_app/parametro/confirmar_exclusao.html"
