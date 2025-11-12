"""
Tudo o que é relativo às views de Categoria de Parametro ficam aqui
"""

from django.urls import reverse_lazy
from django.views.generic import CreateView, DeleteView, ListView, UpdateView

from ..forms import CategoriaParametroForm
from ..models import CategoriaParametro
from .mixins import DeleteRecordMixin


class CategoriaParametroViewMixin:
    """
    Mixin para views de CategoriaParametro: define model, form e URL de sucesso.
    """

    model = CategoriaParametro
    form_class = CategoriaParametroForm
    success_url = reverse_lazy("categoria_parametro_listar")


class CategoriaParametroListView(CategoriaParametroViewMixin, ListView):
    # context_object_name = "categoria_parametro"
    template_name = "simplims_app/categoria_parametro/lista.html"


class CategoriaParametroCreateView(CategoriaParametroViewMixin, CreateView):
    template_name = "simplims_app/categoria_parametro/formulario.html"


class CategoriaParametroUpdateView(CategoriaParametroViewMixin, UpdateView):
    template_name = "simplims_app/categoria_parametro/formulario.html"


class CategoriaParametroDeleteView(
    CategoriaParametroViewMixin, DeleteRecordMixin, DeleteView
):
    template_name = "simplims_app/categoria_parametro/confirmar_exclusao.html"
