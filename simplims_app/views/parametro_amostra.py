from django.shortcuts import get_object_or_404, redirect, render
from django.views import View

from ..models import Amostra, ParametroAmostra
from .mixins import DeleteRecordMixin  # se for usar depois


class ParametroAmostraViewMixin:
    """
    Mixin para views de ParametroAmostra: define amostra,
    contextos e template base.
    """

    model = ParametroAmostra
    template_name = "simplims_app/amostra/parametros_amostra.html"

    def get_amostra(self):
        amostra_id = self.kwargs.get("pk")
        return get_object_or_404(Amostra, pk=amostra_id)


class ParametroAmostraListUpdateView(ParametroAmostraViewMixin, View):
    """
    Exibe os parâmetros da amostra e permite atualizar 'analisar' e 'resultado'.
    """

    def get(self, request, pk):
        amostra = self.get_amostra()

        parametros = ParametroAmostra.objects.filter(
            amostra=amostra
        ).select_related("parametro")

        return render(request, self.template_name, {
            "amostra": amostra,
            "parametros": parametros,
        })

    def post(self, request, pk):
        amostra = get_object_or_404(Amostra, pk=pk)

        parametros = ParametroAmostra.objects.filter(
            amostra=amostra
        )

        for pa in parametros:
            pa.analisar = f"analisar_{pa.id}" in request.POST
            pa.resultado = request.POST.get(f"resultado_{pa.id}", "")
            pa.save()

        return redirect("amostra_listar")

