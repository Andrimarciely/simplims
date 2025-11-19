import locale
from datetime import date, datetime, timedelta
from django.shortcuts import render
from django.db.models import Count, Q

from ..models.ordem_servico import OrdemServico
from ..models.visita_tecnica import VisitaTecnica
from ..models.amostra import Amostra
from ..models.parametro_amostra import ParametroAmostra

from .empresa import (
    EmpresaCreateView,
    EmpresaDeleteView,
    EmpresaListView,
    EmpresaUpdateView,
)
from .legislacao import (
    LegislacaoCreateView,
    LegislacaoDeleteView,
    LegislacaoListView,
    LegislacaoUpdateView,
)
from .matriz import MatrizCreateView, MatrizDeleteView, MatrizListView, MatrizUpdateView

from .ordem_servico import (
    OrdemServicoCreateView,
    OrdemServicoDeleteView,
    OrdemServicoListView,
    OrdemServicoUpdateView,
    OrdemServicoAnaliseView
)
from .categoria_parametro import (
    CategoriaParametroCreateView,
    CategoriaParametroDeleteView,
    CategoriaParametroListView,
    CategoriaParametroUpdateView,
)
from .tipo_parametro import (
    TipoParametroCreateView,
    TipoParametroDeleteView,
    TipoParametroListView,
    TipoParametroUpdateView,
)
from .parametro import (
    ParametroCreateView,
    ParametroDeleteView,
    ParametroListView,
    ParametroUpdateView,
)
from .servico import (
    ServicoCreateView,
    ServicoDeleteView,
    ServicoListView,
    ServicoUpdateView,
)

from .visita_tecnica import (
    VisitaTecnicaCreateView,
    VisitaTecnicaDeleteView,
    VisitaTecnicaListView,
    VisitaTecnicaUpdateView,
    AgendaDiaView,
)

from .amostra import (
    AmostraCreateView,
    AmostraDeleteView,
    AmostraListView,
    AmostraUpdateView,
)

from .servico_contratado import (
    ServicoContratadoCreateView,
    ServicoContratadoDeleteView,
    ServicoContratadoListView,
    ServicoContratadoUpdateView,
)

from.parametro_amostra import (
    ParametroAmostraViewMixin,
    ParametroAmostraListUpdateView,

)

from .plotar_grafico import plotar_grafico

from .relatorio import OrdemServicoRelatorioPDFView

locale.setlocale(locale.LC_TIME, "pt_BR.UTF-8")


def home(request):
    hoje = date.today()
    ano = hoje.year
    mes = hoje.month

    # Cards
    total_os_mes = OrdemServico.objects.filter(
        data_emissao__year=ano,
        data_emissao__month=mes
    ).count()

    visitas_pendentes = VisitaTecnica.objects.filter(
        status="PENDENTE",
        data_visita__gte=hoje
    ).count()

    amostras_hoje = Amostra.objects.filter(
        data_coleta=hoje
    ).count()

    pendentes_analise = ParametroAmostra.objects.filter(
        Q(resultado__isnull=True) | Q(resultado="")
    ).count()

    # Próximas visitas
    proximas_visitas = VisitaTecnica.objects.filter(
        data_visita__gte=hoje
    ).order_by("data_visita", "hora_visita")[:5]

    # Gráfico: amostras por mês
    amostras_por_mes = (
        Amostra.objects.filter(data_coleta__year=ano)
        .values("data_coleta__month")
        .annotate(total=Count("id"))
        .order_by("data_coleta__month")
    )

    labels = list(range(1, 13))
    valores = [
        next((item["total"] for item in amostras_por_mes if item["data_coleta__month"] == mes), 0)
        for mes in labels
    ]

    context = {
        "total_os_mes": total_os_mes,
        "visitas_pendentes": visitas_pendentes,
        "amostras_hoje": amostras_hoje,
        "pendentes_analise": pendentes_analise,
        "proximas_visitas": proximas_visitas,
        "grafico_labels": labels,
        "grafico_valores": valores,
    }

    return render(request, "dashboard.html", context)
