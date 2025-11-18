import io
import base64
import matplotlib.pyplot as plt

from django.shortcuts import render
from ..forms import GraficoFiltroForm
from ..models import Amostra, ParametroAmostra


def plotar_grafico(request):
    form = GraficoFiltroForm(request.GET or None)
    grafico_base64 = None

    if form.is_valid():
        ano = form.cleaned_data["ano"]
        local = form.cleaned_data["local"]
        parametro = form.cleaned_data["parametro"]

        # Filtra as amostras pelo ano e local
        amostras = (
            Amostra.objects.filter(
                data_coleta__year=ano,
                servico_contratado__local=local
            )
            .order_by("data_coleta")
        )

        # Filtra os valores daquele parâmetro nessas amostras
        resultados = (
            ParametroAmostra.objects.filter(
                amostra__in=amostras,
                parametro=parametro
            )
            .select_related("amostra")
            .order_by("amostra__data_coleta")
        )

        datas = []
        valores = []

        for r in resultados:
            if r.resultado:
                try:
                    valor = float(r.resultado.replace(",", "."))
                    valores.append(valor)
                    datas.append(r.amostra.data_coleta)
                except ValueError:
                    # Ignora valores não numéricos
                    pass

        if datas:
            fig, ax = plt.subplots(figsize=(10, 4))
            ax.plot(datas, valores, marker="o")
            ax.set_title(f"{parametro.descricao} – {local} ({ano})")
            ax.set_xlabel("Data da coleta")
            ax.set_ylabel("Resultado")
            ax.grid(True)

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
