"""
Tudo o que é relativo às views de VisitaTecnica ficam aqui
"""

from django.urls import reverse_lazy
from django.views.generic import CreateView, DeleteView, ListView, UpdateView
from datetime import date, timedelta
from django.utils import timezone
from django.shortcuts import render

from ..forms import VisitaTecnicaForm
from ..models import VisitaTecnica
from .mixins import DeleteRecordMixin
from ..models import VisitaTecnica


class AgendaDiaView(ListView):
    template_name = "simplims_app/visita_tecnica/agenda.html"

    def get(self, request, ano=None, mes=None, dia=None):
        # Se não passar data -> usa hoje
        if ano and mes and dia:
            data = timezone.datetime(int(ano), int(mes), int(dia)).date()
        else:
            data = timezone.localdate()

        visitas = VisitaTecnica.objects.filter(data_visita=data).order_by("hora_visita")

        contexto = {
            "data": data,
            "visitas": visitas,
            "anterior": data - timedelta(days=1),
            "proximo": data + timedelta(days=1),
        }
        return render(request, self.template_name, contexto)


class VisitaTecnicaViewMixin:
    """
    Mixin para views de VisitaTecnica: define model, form e URL de sucesso.
    """

    model = VisitaTecnica
    form_class = VisitaTecnicaForm
    success_url = reverse_lazy("visita_tecnica_listar")


class VisitaTecnicaListView(VisitaTecnicaViewMixin, ListView):
    # context_object_name = "visita_tecnica"
    template_name = "simplims_app/visita_tecnica/lista.html"


class VisitaTecnicaCreateView(VisitaTecnicaViewMixin, CreateView):
    template_name = "simplims_app/visita_tecnica/formulario.html"


class VisitaTecnicaUpdateView(VisitaTecnicaViewMixin, UpdateView):
    template_name = "simplims_app/visita_tecnica/formulario.html"


class VisitaTecnicaDeleteView(VisitaTecnicaViewMixin, DeleteRecordMixin, DeleteView):
    template_name = "simplims_app/visita_tecnica/confirmar_exclusao.html"
