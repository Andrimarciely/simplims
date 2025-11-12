from django.urls import reverse_lazy
from django.views.generic import CreateView, DeleteView, ListView, UpdateView

from ..forms import EmpresaForm
from ..models import Empresa
from .mixins import DeleteRecordMixin


class EmpresaViewMixin:
    """
    Mixin para views de Empresa: define model, form e URL de sucesso.
    """

    model = Empresa
    form_class = EmpresaForm
    success_url = reverse_lazy("empresa_listar")


class EmpresaListView(EmpresaViewMixin, ListView):
    # context_object_name = "empresa"
    template_name = "simplims_app/empresa/lista.html"


class EmpresaCreateView(EmpresaViewMixin, CreateView):
    template_name = "simplims_app/empresa/formulario.html"


class EmpresaUpdateView(EmpresaViewMixin, UpdateView):
    template_name = "simplims_app/empresa/formulario.html"


class EmpresaDeleteView(EmpresaViewMixin, DeleteRecordMixin, DeleteView):
    template_name = "simplims_app/empresa/confirmar_exclusao.html"
