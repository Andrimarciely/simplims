import calendar
import locale
from calendar import HTMLCalendar
from datetime import datetime, timedelta

from django.shortcuts import render

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
    OrdemServicoResultadosUpdateView,
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

locale.setlocale(locale.LC_TIME, "pt_BR.UTF-8")


def home(request, ano=None, mes=None):
    nome = "Andrimarciely"

    data_corrente = datetime.now()

    if not ano:
        ano = data_corrente.year

    if not mes:
        mes = data_corrente.month

    data_do_calendario = datetime(ano, mes, 1)

    return render(
        request,
        "home.html",
        {
            "nome": nome,
            "data_corrente": data_corrente,
            "data_calendario": data_do_calendario,
        },
    )
