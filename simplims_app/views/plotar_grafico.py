import io
import base64
import matplotlib.pyplot as plt

from django.shortcuts import render
from ..forms import GraficoFiltroForm
from ..models import Amostra, ParametroAmostra, Legislacao


def plotar_grafico(request):
    form = GraficoFiltroForm(request.GET or None)
    grafico_base64 = None

    if form.is_valid():
        ano = form.cleaned_data["ano"]
        local = form.cleaned_data["local"]
        parametro = form.cleaned_data["parametro"]

        # Legislacao do parâmetro
        legislacao = Legislacao.objects.filter(parametro=parametro).first()
        valor_legislacao = legislacao.valor_maximo if legislacao else None

        # Filtra amostras do ano e local
        amostras = (
            Amostra.objects.filter(
                data_coleta__year=ano,
                servico_contratado__local=local
            )
            .order_by("data_coleta")
        )

        # ---------- COLETAR MONTANTE ----------
        amostras_montante = amostras.filter(tipo_ponto="MONTANTE")
        resultados_montante = (
            ParametroAmostra.objects.filter(
                amostra__in=amostras_montante,
                parametro=parametro
            )
            .select_related("amostra")
            .order_by("amostra__data_coleta")
        )

        datas_M = []
        valores_M = []

        for r in resultados_montante:
            if r.resultado:
                try:
                    valor = float(r.resultado.replace(",", "."))
                    datas_M.append(r.amostra.data_coleta)
                    valores_M.append(valor)
                except ValueError:
                    pass

        # ---------- COLETAR JUSANTE ----------
        amostras_jusante = amostras.filter(tipo_ponto="JUSANTE")
        resultados_jusante = (
            ParametroAmostra.objects.filter(
                amostra__in=amostras_jusante,
                parametro=parametro
            )
            .select_related("amostra")
            .order_by("amostra__data_coleta")
        )

        datas_J = []
        valores_J = []

        for r in resultados_jusante:
            if r.resultado:
                try:
                    valor = float(r.resultado.replace(",", "."))
                    datas_J.append(r.amostra.data_coleta)
                    valores_J.append(valor)
                except ValueError:
                    pass

        # ---------- PLOTAR SE TIVER ALGUM OS DOIS ----------
        if datas_M or datas_J or valor_legislacao:

            fig, ax = plt.subplots(figsize=(10, 4))

            # Montante
            if datas_M:
                ax.plot(datas_M, valores_M, marker="o", label="Montante")

            # Jusante
            if datas_J:
                ax.plot(datas_J, valores_J, marker="o", label="Jusante")

            # Legislação (reta horizontal)
            if valor_legislacao:
                ax.axhline(y=valor_legislacao, linestyle='--', label=f"Legislação ({valor_legislacao})")

            ax.set_title(f"{parametro.descricao} – {local} ({ano})")
            ax.set_xlabel("Data da coleta")
            ax.set_ylabel("Resultado")
            ax.grid(True)
            ax.legend()

            buffer = io.BytesIO()
            plt.savefig(buffer, format="png")
            buffer.seek(0)
            grafico_base64 = base64.b64encode(buffer.getvalue()).decode()
            plt.close()

    return render(
        request,
        "simplims_app/grafico/plotar.html",
        {"form": form, "grafico": grafico_base64},
    )
