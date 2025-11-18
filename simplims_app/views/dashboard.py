from datetime import date
from django.db.models import Count, Q
from django.shortcuts import render
from .models import OrdemServico, Amostra, ParametroAmostra, VisitaTecnica

def dashboard(request):
    hoje = date.today()
    ano = hoje.year
    mes = hoje.month

    # 1. Total OS do mês
    total_os_mes = OrdemServico.objects.filter(
        data_emissao__year=ano,
        data_emissao__month=mes
    ).count()

    # 2. Visitas pendentes
    visitas_pendentes = VisitaTecnica.objects.filter(
        status="PENDENTE",
        data_visita__gte=hoje
    ).count()

    # 3. Amostras coletadas hoje
    amostras_hoje = Amostra.objects.filter(
        data_coleta=hoje
    ).count()

    # 4. Amostras pendentes de análise (sem resultado)
    pendentes_analise = ParametroAmostra.objects.filter(
        Q(resultado__isnull=True) | Q(resultado="")
    ).count()

    # 5. Próximas visitas (agenda)
    proximas_visitas = VisitaTecnica.objects.filter(
        data_visita__gte=hoje
    ).order_by("data_visita", "hora_visita")[:5]

    # 6. Gráfico: amostras por mês no ano
    amostras_por_mes = (
        Amostra.objects.filter(data_coleta__year=ano)
        .values("data_coleta__month")
        .annotate(total=Count("id"))
        .order_by("data_coleta__month")
    )

    # Transformar em arrays para o Chart.js
    labels = []
    valores = []
    for i in range(1, 13):
        labels.append(i)
        valores.append(
            next((item["total"] for item in amostras_por_mes if item["data_coleta__month"] == i), 0)
        )

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
