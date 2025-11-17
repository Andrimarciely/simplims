from django.urls import reverse_lazy
from django.views.generic import CreateView, DeleteView, ListView, UpdateView
from django.shortcuts import render, get_object_or_404
from django.views import View

from ..forms import OrdemServicoForm
from ..models import OrdemServico, Amostra, ParametroAmostra, Legislacao
from .mixins import DeleteRecordMixin


# ============================================================
#  MIXIN PADRÃO DAS VIEWS DE ORDEM DE SERVIÇO
# ============================================================

class OrdemServicoViewMixin:
    """
    Mixin base para views de Ordem de Serviço:
    - define model
    - define form
    - define URL de sucesso
    """
    model = OrdemServico
    form_class = OrdemServicoForm
    ordering = ['-id']
    success_url = reverse_lazy("ordem_servico_listar")


# ============================================================
#  CRUD
# ============================================================

class OrdemServicoListView(OrdemServicoViewMixin, ListView):
    template_name = "simplims_app/ordem_servico/lista.html"


class OrdemServicoCreateView(OrdemServicoViewMixin, CreateView):
    template_name = "simplims_app/ordem_servico/formulario.html"


class OrdemServicoUpdateView(OrdemServicoViewMixin, UpdateView):
    template_name = "simplims_app/ordem_servico/formulario.html"


class OrdemServicoDeleteView(OrdemServicoViewMixin, DeleteRecordMixin, DeleteView):
    template_name = "simplims_app/ordem_servico/confirmar_exclusao.html"


# ============================================================
#  MIXIN DE ANÁLISE CONSOLIDADA DA ORDEM DE SERVIÇO
# ============================================================

class OrdemServicoAnaliseMixin:
    template_name = "simplims_app/ordem_servico/analise.html"

    def montar_analise(self, ordem_servico):
        from simplims_app.models import ParametroAmostra, Legislacao

        # 🔥 CORREÇÃO AQUI:
        amostras = Amostra.objects.filter(
            servico_contratado__ordem_servico=ordem_servico
        ).order_by("identificacao")

        analise_os = []

        for amostra in amostras:
            parametros_amostra = (
                ParametroAmostra.objects
                .filter(amostra=amostra)
                .select_related("parametro", "parametro__categoria_parametro")
            )

            linhas = []

            for pa in parametros_amostra:
                legislacao = Legislacao.objects.filter(parametro=pa.parametro).first()

                if not pa.resultado:
                    status = "pendente"

                elif legislacao and legislacao.valor_maximo is not None:
                    try:
                        valor = float(pa.resultado)
                        status = "conforme" if valor <= legislacao.valor_maximo else "nao_conforme"
                    except:
                        status = "erro"

                else:
                    status = "sem_limite"

                linhas.append({
                    "pa": pa,
                    "legislacao": legislacao,
                    "status": status,
                })

            analise_os.append({
                "amostra": amostra,
                "linhas": linhas,
            })

        return analise_os


# ============================================================
#  VIEW DE ANÁLISE DA ORDEM DE SERVIÇO (oficial)
# ============================================================

class OrdemServicoAnaliseView(OrdemServicoAnaliseMixin, View):
    """
    View única da análise da Ordem de Serviço.
    Usa o mixin acima para montar os dados.
    """

    def get(self, request, pk):
        os = get_object_or_404(OrdemServico, pk=pk)

        analise_os = self.montar_analise(os)

        return render(request, self.template_name, {
            "os": os,
            "analise_os": analise_os,
        })
