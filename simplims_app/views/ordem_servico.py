"""
Tudo o que é relativo às views de OrdemServico ficam aqui
"""

from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView, DeleteView, ListView, UpdateView
from django.db.models import Q

from ..forms import OrdemServicoForm, customize_ordem_servico_resultado_form
from ..models import OrdemServico
from .mixins import DeleteRecordMixin


class OrdemServicoViewMixin:
    """
    Mixin para views de OrdemServico: define model, form e URL de sucesso.
    """

    model = OrdemServico
    form_class = OrdemServicoForm
    success_url = reverse_lazy("ordem_servico_listar")

    def get_queryset(self):
        return OrdemServico.objects.order_by('-id')


class OrdemServicoListView(OrdemServicoViewMixin, ListView):
    # context_object_name = "ordem_servico"
    template_name = "simplims_app/ordem_servico/lista.html"

    def get_queryset(self):
        qs = super().get_queryset()

        termo = self.request.GET.get("q")
        if termo:
            qs = qs.filter(
                Q(id__icontains=termo) |
                Q(empresa__apelido__icontains=termo) |
                Q(observacoes__icontains=termo)
            )

        return qs

class OrdemServicoCreateView(OrdemServicoViewMixin, CreateView):
    template_name = "simplims_app/ordem_servico/formulario.html"


class OrdemServicoUpdateView(OrdemServicoViewMixin, UpdateView):
    template_name = "simplims_app/ordem_servico/formulario.html"


class OrdemServicoDeleteView(OrdemServicoViewMixin, DeleteRecordMixin, DeleteView):
    template_name = "simplims_app/ordem_servico/confirmar_exclusao.html"


class OrdemServicoResultadosUpdateView(OrdemServicoViewMixin, UpdateView):
    template_name = "simplims_app/ordem_servico/formulario_resultados.html"

    def __build_form_class(self, record):
        results = record.resultados_servicos
        field_list = [
            {
                "field": str(s.pk),
                "label": s.descricao,
                "initial": results.get(str(s.pk)) if results else "",
            }
            for s in record.servicos.all()
        ]
        self.form_class = customize_ordem_servico_resultado_form(field_list)

    def get(self, request, *args, **kwargs):
        pk = kwargs.get("pk")
        record = get_object_or_404(self.model, pk=pk)

        self.__build_form_class(record)

        return super().get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        pk = kwargs.get("pk")
        record = get_object_or_404(self.model, pk=pk)

        record.resultados_servicos = {
            k: v for k, v in request.POST.items() if k.isdigit()
        }
        record.save()

        return redirect(self.success_url)
