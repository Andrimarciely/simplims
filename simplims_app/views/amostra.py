from django.urls import reverse_lazy
from django.views.generic import CreateView, DeleteView, ListView, UpdateView

from ..forms import AmostraForm
from ..models import Amostra
from .mixins import DeleteRecordMixin


class AmostraViewMixin:
    """
    Mixin para views de Amostra: define model, form e URL de sucesso.
    """
    model = Amostra
    form_class = AmostraForm
    success_url = reverse_lazy("amostra_listar")


class AmostraListView(AmostraViewMixin, ListView):
    # context_object_name = "amostra"
    template_name = "simplims_app/amostra/lista.html"


class AmostraCreateView(AmostraViewMixin, CreateView):
    template_name = "simplims_app/amostra/formulario.html"


class AmostraUpdateView(AmostraViewMixin, UpdateView):
    template_name = "simplims_app/amostra/formulario.html"


class AmostraDeleteView(AmostraViewMixin, DeleteRecordMixin, DeleteView):
    template_name = "simplims_app/amostra/confirmar_exclusao.html"