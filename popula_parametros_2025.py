import random
from simplims_app.models import Amostra, Parametro, ParametroAmostra, Legislacao

param_ids = [21,22,1,2,6,25,35,36,37,38,39,40,41,42,43,45,46,47,48,49,50,52,53,54]

leg_map = {l.parametro_id: l.valor_maximo for l in Legislacao.objects.filter(parametro_id__in=param_ids)}
params = {p.id: p for p in Parametro.objects.filter(id__in=param_ids)}

amostras = Amostra.objects.filter(id__in=[40001,40002,40003,40004,40005,40006,40007,40008])

count = 0

for am in amostras:
    mes = am.data_coleta.month
    jus = (am.tipo_ponto == "JUSANTE")
    saz = 0.9 + 0.02 * mes

    for pid in param_ids:
        limit = leg_map.get(pid)
        if limit is None:
            continue

        if not jus:
            val = limit * saz * random.uniform(0.2, 0.6)
        else:
            val = limit * saz * random.uniform(0.4, 0.9)
            if random.random() < 0.4:
                val = limit * random.uniform(1.05, 1.6)

        if pid in (21, 22):
            resultado = str(max(int(round(val)), 1))
        else:
            resultado = f"{max(val, limit * 0.01):.5f}"

        ParametroAmostra.objects.update_or_create(
            amostra=am,
            parametro=params[pid],
            defaults={"analisar": True, "resultado": resultado},
        )
        count += 1

print("ParametroAmostra criados/atualizados:", count)
