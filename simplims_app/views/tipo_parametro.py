"""
Tudo o que é relativo às views de Tipo de Parametro ficam aqui
"""

from django.urls import reverse_lazy
from django.views.generic import CreateView, DeleteView, ListView, UpdateView

from ..forms import TipoParametroForm
from ..models import TipoParametro
from .mixins import DeleteRecordMixin


class TipoParametroViewMixin:
    """
    Mixin para views de TipoParametro: define model, form e URL de sucesso.
    """

    model = TipoParametro
    form_class = TipoParametroForm
    success_url = reverse_lazy("tipo_parametro_listar")


class TipoParametroListView(TipoParametroViewMixin, ListView):
    # context_object_name = "tipo_parametro"
    template_name = "simplims_app/tipo_parametro/lista.html"


class TipoParametroCreateView(TipoParametroViewMixin, CreateView):
    template_name = "simplims_app/tipo_parametro/formulario.html"


class TipoParametroUpdateView(TipoParametroViewMixin, UpdateView):
    template_name = "simplims_app/tipo_parametro/formulario.html"


class TipoParametroDeleteView(TipoParametroViewMixin, DeleteRecordMixin, DeleteView):
    template_name = "simplims_app/tipo_parametro/confirmar_exclusao.html"
